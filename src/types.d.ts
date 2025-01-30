interface FileSystem {
  readFile(path: string, options: { encoding: string }): Promise<string>;
  readFile(path: string, options?: { encoding?: undefined }): Promise<Uint8Array>;
}

declare interface Window {
  fs: FileSystem;
}