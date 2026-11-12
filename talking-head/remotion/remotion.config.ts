import { Config } from "@remotion/cli/config";
// Chromium yang sudah terpasang di container cloud (di PC Endrich baris ini boleh dihapus; Remotion pakai Chrome sendiri)
if (process.platform === "linux") Config.setBrowserExecutable("/opt/pw-browsers/chromium-1243/chrome-linux64/chrome");
Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
