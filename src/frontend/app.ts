type HealthResponse = {
  status: string;
};

const STATUS_OK = "Ready";
const STATUS_UNAVAILABLE = "Unavailable";

function setBackendStatus(message: string, className: "is-ok" | "is-bad"): void {
  const status = document.querySelector<HTMLDListElement>("#backend-status");

  if (!status) {
    return;
  }

  status.textContent = message;
  status.classList.remove("is-ok", "is-bad");
  status.classList.add(className);
}

async function readHealth(): Promise<HealthResponse> {
  const response = await fetch("/health", {
    headers: {
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Health check failed with ${response.status}`);
  }

  return response.json() as Promise<HealthResponse>;
}

async function refreshBackendStatus(): Promise<void> {
  try {
    const health = await readHealth();

    if (health.status !== "ok") {
      setBackendStatus(STATUS_UNAVAILABLE, "is-bad");
      return;
    }

    setBackendStatus(STATUS_OK, "is-ok");
  } catch {
    setBackendStatus(STATUS_UNAVAILABLE, "is-bad");
  }
}

void refreshBackendStatus();
