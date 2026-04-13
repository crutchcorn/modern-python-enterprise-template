import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterAll, afterEach, beforeAll } from "vitest";
import { worker } from './server'

beforeAll(async () => {
  await worker.start();
});

afterEach(() => {
  worker.resetHandlers();
  cleanup();
});

afterAll(() => worker.stop());
