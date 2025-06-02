import React, { useEffect, useState, useRef } from "react";
import ListGroup from "./componenets/ListGroup";

interface Song {
  uuid: number;
  name: string;
  artist: string;
}

function Songs() {
  const [songs, setSongs] = useState<Song[]>([]);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [playingId, setPlayingId] = useState<number | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0); // seconds
  const [duration, setDuration] = useState(0); // seconds
  const progressRef = useRef(false); // to detect if user is dragging the slider

  useEffect(() => {
    fetch("http://localhost:8080/songs")
      .then((res) => res.json())
      .then((data: Song[]) => setSongs(data))
      .catch((err) => console.error("Failed to fetch songs:", err));
  }, []);

  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, []);

  const playSong = (uuid: number) => {
    if (audioRef.current) {
      // If same song clicked, just play it (if paused)
      if (playingId === uuid) {
        if (!isPlaying) {
          audioRef.current
            .play()
            .catch((err) => console.error("Playback failed:", err));
          setIsPlaying(true);
        }
        return;
      }

      // Different song clicked, stop previous
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      audioRef.current.removeEventListener("timeupdate", onTimeUpdate);
      audioRef.current.removeEventListener("loadedmetadata", onLoadedMetadata);
    }

    // Play new song
    const audio = new Audio(`http://localhost:8080/songs/${uuid}`);
    audio.addEventListener("loadedmetadata", onLoadedMetadata);
    audio.addEventListener("timeupdate", onTimeUpdate);
    audio.play().catch((err) => console.error("Playback failed:", err));
    audioRef.current = audio;
    setPlayingId(uuid);
    setIsPlaying(true);
  };

  const playPauseSong = (uuid: number) => {
    if (audioRef.current && playingId === uuid) {
      if (isPlaying) {
        audioRef.current.pause();
        setIsPlaying(false);
      } else {
        audioRef.current
          .play()
          .catch((err) => console.error("Playback failed:", err));
        setIsPlaying(true);
      }
    } else {
      // Play new song if not current
      playSong(uuid);
    }
  };

  const onLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
    }
  };

  const onTimeUpdate = () => {
    if (!progressRef.current && audioRef.current) {
      setProgress(audioRef.current.currentTime);
    }
  };

  const stopSong = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      audioRef.current.removeEventListener("timeupdate", onTimeUpdate);
      audioRef.current.removeEventListener("loadedmetadata", onLoadedMetadata);
      audioRef.current = null;
    }
    setPlayingId(null);
    setIsPlaying(false);
    setProgress(0);
    setDuration(0);
  };

  const onSeekChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTime = Number(e.target.value);
    setProgress(newTime);
  };

  const onSeekMouseDown = () => {
    progressRef.current = true;
  };

  const onSeekMouseUp = (e: React.MouseEvent<HTMLInputElement>) => {
    if (audioRef.current) {
      const target = e.target as HTMLInputElement;
      const newTime = Number(target.value);
      audioRef.current.currentTime = newTime;
    }
    progressRef.current = false;
  };

  const items = songs.map((song) => ({
    id: song.uuid,
    label: `${song.name} - ${song.artist}`,
  }));

  return (
    <div>
      <h2>Songs</h2>
      <ListGroup
        items={items}
        heading="Songs"
        renderRight={(item) => (
            <button
              className="bg-dark text-white mr-2"
              onClick={(e) => {
                e.stopPropagation();
                playSong(item.id);
              }}
            >
              ▶️
            </button>
        )}
      />

      {playingId !== null && (
        <div style={{ marginTop: "3rem" }}>
          {/* Current song info */}
          <div style={{ marginBottom: "0.5rem", fontWeight: "bold" }}>
            {songs.find((s) => s.uuid === playingId)?.name} -{" "}
            {songs.find((s) => s.uuid === playingId)?.artist}
          </div>

          {/* Progress slider */}
          <input
            type="range"
            min={0}
            max={duration}
            value={progress}
            step="0.1"
            onChange={onSeekChange}
            onMouseDown={onSeekMouseDown}
            onMouseUp={onSeekMouseUp}
            style={{ width: "100%" }}
          />
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              marginBottom: "1rem",
            }}
          >
            <small>{formatTime(progress)}</small>
            <small>{formatTime(duration)}</small>
          </div>

          {/* Controls below progress bar */}
          <div>
            <button
              className="bg-dark text-white mr-2"
              onClick={() => {
                if (playingId !== null) playPauseSong(playingId);
              }}
            >
              {isPlaying ? "⏸️ Pause" : "▶️ Play"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function formatTime(seconds: number) {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, "0")}`;
}

export default Songs;
