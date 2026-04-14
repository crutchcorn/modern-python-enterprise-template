import { useMemo } from "react";

const getBaseUrl = (env: ImportMetaEnv) => {
  return env.VITE_BACKEND_BASE_URL ?? `http://localhost:8000`;
};

export const useNetworkingParams = () => {
  const env = import.meta.env;

  const baseUrl = useMemo(() => {
    if (!env) return "";
    return getBaseUrl(env);
  }, [env]);

  return { baseUrl } as const;
};
