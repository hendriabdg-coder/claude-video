// SATU-SATUNYA file yang diisi per video. Waktu dalam detik (dari video talking head asli).
// type "hybrid" = talking head + motion (variant: split | pip | lower); type "full" = full Remotion (variant: kinetic | stat | list | quote).
// Audio talking head selalu jalan dari awal sampai akhir; segmen "full" hanya mengganti gambarnya.
export type Seg =
  | { type: "hybrid"; variant: "split" | "pip" | "lower"; from: number; to: number; label?: string; title: string; accent?: string; points?: string[] }
  | { type: "full"; variant: "kinetic"; from: number; to: number; words: string[] }
  | { type: "full"; variant: "stat"; from: number; to: number; value: number; prefix?: string; suffix?: string; decimals?: number; label: string; source?: string; bars?: [string, number][] }
  | { type: "full"; variant: "list"; from: number; to: number; title: string; items: string[] }
  | { type: "full"; variant: "quote"; from: number; to: number; quote: string; source: string };

export const VIDEO = "th.mp4";   // taruh video 16:9 di public/th.mp4
export const SERIES = "ENDRICHTECH";

// CONTOH (placeholder 30 dtk) — diganti setelah video Endrich masuk dan ditranskrip.
export const SEGMENTS: Seg[] = [
  { type: "full", variant: "kinetic", from: 0, to: 3, words: ["AKU", "BUKAN", "PROGRAMMER"] },
  { type: "hybrid", variant: "split", from: 3, to: 9, label: "BAGIAN 1", title: "Bikin website pakai AI", accent: "AI", points: ["Cukup jelaskan idenya", "AI tulis kodenya", "Kamu cek hasilnya"] },
  { type: "full", variant: "stat", from: 9, to: 14, value: 28.65, decimals: 2, suffix: " JT", label: "secret baru terdeteksi di commit GitHub publik 2025", source: "GitGuardian, State of Secrets Sprawl 2026" },
  { type: "hybrid", variant: "pip", from: 14, to: 19, label: "BAGIAN 2", title: "Jangan taruh API key di front-end", accent: "front-end" },
  { type: "full", variant: "list", from: 19, to: 24, title: "3 langkah aman", items: ["Simpan di back-end", "Batasi akses key", "Rotasi kalau bocor"] },
  { type: "hybrid", variant: "lower", from: 24, to: 27.5, title: "Follow buat part 2", accent: "part 2" },
  { type: "full", variant: "quote", from: 27.5, to: 30, quote: "Mulai dari satu ide.", source: "EndrichTech" },
];
