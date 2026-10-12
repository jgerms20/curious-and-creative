"""Host adapters: get an episode's audio onto a public URL.

  HostAdapter.publish(episode, audio_path) -> public URL of the audio
  LocalHost(out_dir)                       copies into data/public/audio (serve that folder anywhere)
  TransistorHost(api_key, show_id)         uploads through the Transistor API (verify before enabling)

The base class refuses any episode whose stored gate decision is not PUBLISH (standards
AUTO-2 / NE-13). There is no flag to override it: fix the episode, not the check.
"""
from __future__ import annotations

import json
import os
import shutil
import urllib.error
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod
from pathlib import Path

from earlobe.publish import coerce, disclosure_text, public_base_url, public_dir
from earlobe.publish.notes import notes_html
from earlobe.schemas import Episode

TRANSISTOR_API = "https://api.transistor.fm/v1"


class HostError(RuntimeError):
    """The hosting service failed or answered with something unexpected."""


class PublishRefused(RuntimeError):
    """The episode did not pass the gate, so no host will take it."""


def require_publishable(episode: Episode) -> None:
    """Only an episode whose gate decision is PUBLISH may go to a host. No override."""
    decision = (episode.gate or {}).get("decision")
    if decision != "PUBLISH" or episode.status in ("retracted", "killed"):
        raise PublishRefused(f"episode {episode.id} has gate decision {decision!r} and status "
                             f"{episode.status!r}; only a PUBLISH decision may be published")


class HostAdapter(ABC):
    """Interface: publish(episode, audio_path) -> public URL of the audio."""

    name = ""

    def publish(self, episode, audio_path) -> str:
        episode = coerce(Episode, episode)
        require_publishable(episode)
        path = Path(audio_path)
        if not path.is_file():
            raise FileNotFoundError(f"audio file not found: {audio_path}")
        return self._publish(episode, path)

    @abstractmethod
    def _publish(self, episode: Episode, audio_path: Path) -> str: ...


# ---------------------------------------------------------------- local
def _copy(src: Path, dest: Path) -> None:
    """Copy via a temp name so a half-written file is never served. No-op if src is dest."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.resolve() == src.resolve():
        return
    part = dest.with_name(dest.name + ".part")
    shutil.copyfile(src, part)
    os.replace(part, dest)


class LocalHost(HostAdapter):
    """Copy audio to <out_dir>/<episode id>.mp3 (default data/public/audio).

    The returned URL is <base>/audio/<file>, so serving data/public/ as the site root makes
    it live. A transcript file named on the episode is copied to ../transcripts/.
    """

    name = "local"

    def __init__(self, out_dir: str | Path | None = None, base_url: str | None = None):
        self.out_dir = Path(out_dir) if out_dir else public_dir("audio")
        self.base_url = base_url

    def _publish(self, episode: Episode, audio_path: Path) -> str:
        name = f"{episode.id}{audio_path.suffix or '.mp3'}"
        _copy(audio_path, self.out_dir / name)
        transcript = Path(episode.transcript_path) if episode.transcript_path else None
        if transcript and transcript.is_file():
            _copy(transcript, self.out_dir.parent / "transcripts" / transcript.name)
        return f"{public_base_url(self.base_url)}/audio/{name}"


# ---------------------------------------------------------------- Transistor
def _http(method: str, url: str, *, headers: dict | None = None, data: bytes | None = None,
          timeout: int = 120) -> tuple[int, bytes]:
    """The one network call of TransistorHost. Tests replace this."""
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    where = f"{method} {url.split('?')[0]}"          # never log the query: upload URLs are signed
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        raise HostError(f"{where} -> HTTP {e.code}: {e.read()[:200].decode('utf-8', 'replace')}") from None
    except urllib.error.URLError as e:
        raise HostError(f"{where} failed: {e.reason}") from None


class TransistorHost(HostAdapter):
    """Upload through the Transistor API: authorize_upload -> PUT -> create episode -> publish.

    VERIFY vs CURRENT TRANSISTOR API DOCS BEFORE ENABLING. This follows the documented flow
    (base https://api.transistor.fm/v1, header x-api-key) but has not been run against the
    live API: confirm every endpoint path, field name and response key below, and try it on a
    throwaway show first.

    api_key  env TRANSISTOR_API_KEY if not given.
    show_id  the id or slug of the show on Transistor (not the Earlobe show id).
    dry_run  no network; returns a URL on transistor.invalid.

    Returns the episode's media URL (falling back to its share URL).
    """

    name = "transistor"

    def __init__(self, api_key: str | None = None, show_id: str = "", *, base: str = TRANSISTOR_API,
                 dry_run: bool = False):
        self.api_key = api_key or os.environ.get("TRANSISTOR_API_KEY", "")
        self.show_id = show_id
        self.base = base.rstrip("/")
        self.dry_run = dry_run
        if not dry_run and not self.api_key:
            raise ValueError("TRANSISTOR_API_KEY is not set (use the local host, or dry_run=True)")
        if not dry_run and not show_id:
            raise ValueError("show_id (the Transistor show id) is required")

    def _api(self, method: str, path: str, *, params: dict | None = None, form: dict | None = None) -> dict:
        url = self.base + path + ("?" + urllib.parse.urlencode(params) if params else "")
        headers = {"x-api-key": self.api_key, "Accept": "application/json"}
        data = None
        if form is not None:
            data = urllib.parse.urlencode(form).encode("utf-8")
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        _, body = _http(method, url, headers=headers, data=data)
        try:
            return json.loads(body or b"{}")
        except ValueError:
            raise HostError(f"{method} {path}: response was not JSON") from None

    def _publish(self, episode: Episode, audio_path: Path) -> str:
        if self.dry_run:
            return f"https://share.transistor.invalid/{self.show_id or 'show'}/{episode.id}"

        # 1. ask Transistor for a signed upload URL
        auth = self._api("GET", "/episodes/authorize_upload", params={"filename": audio_path.name})
        try:
            attrs = auth["data"]["attributes"]
            upload_url, audio_url = attrs["upload_url"], attrs["audio_url"]
        except KeyError:
            raise HostError("authorize_upload: unexpected response shape") from None

        # 2. PUT the file to the signed URL (no API key on this request: it goes to storage)
        _http("PUT", upload_url, headers={"Content-Type": attrs.get("content_type") or "audio/mpeg"},
              data=audio_path.read_bytes(), timeout=600)

        # 3. create the episode from the uploaded audio (draft)
        notes = notes_html(episode.show_notes_md) if episode.show_notes_md else \
            f"<p>{episode.description}</p><p>{episode.disclosure_text or disclosure_text()}</p>"
        created = self._api("POST", "/episodes", form={
            "episode[show_id]": self.show_id,
            "episode[title]": episode.title,
            "episode[summary]": episode.description,
            "episode[description]": notes,
            "episode[audio_url]": audio_url,
            "episode[explicit]": "false",
        })
        try:
            episode_id = created["data"]["id"]
        except KeyError:
            raise HostError("create episode: unexpected response shape") from None

        # 4. publish it
        done = self._api("PATCH", f"/episodes/{episode_id}/publish", form={"episode[status]": "published"})
        out = (done.get("data") or {}).get("attributes") or {}
        return out.get("media_url") or out.get("share_url") or audio_url
