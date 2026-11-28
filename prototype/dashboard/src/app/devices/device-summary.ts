/** One observation as returned by the backend's `GET /observations`. */
export interface Observation {
  observation_id: string;
  scanner_id: string;
  session_id: string;
  device_id: string | null;
  captured_at: string;
  received_at: string;
  protocol: string;
  observed_address: string | null;
  address_type: string | null;
  rssi_dbm: number | null;
  signal_percent: number | null;
  metadata: Record<string, unknown>;
}

/** One detected device and its most recent observation, as the dashboard shows it. */
export interface DeviceSummary {
  deviceId: string;
  /** Human-readable name, when the backend provides one. */
  displayName: string | null;
  protocol: string;
  rssiDbm: number | null;
  signalPercent: number | null;
  lastSeen: string;
}

/**
 * Reduces raw observations to one row per detected device, using each device's
 * most recent observation. Observations not linked to a device are skipped,
 * because they are not a detected device yet. Newest devices come first.
 *
 * Temporary: the device list endpoint from #139 will return these rows directly,
 * including display names. Until then display names are unavailable.
 */
export function summarizeDevices(observations: Observation[]): DeviceSummary[] {
  const latest = new Map<string, Observation>();
  for (const o of observations) {
    if (!o.device_id) continue;
    const current = latest.get(o.device_id);
    if (!current || Date.parse(o.captured_at) > Date.parse(current.captured_at)) {
      latest.set(o.device_id, o);
    }
  }
  return [...latest.values()]
    .sort((a, b) => Date.parse(b.captured_at) - Date.parse(a.captured_at))
    .map((o) => ({
      deviceId: o.device_id as string,
      displayName: null,
      protocol: o.protocol,
      rssiDbm: o.rssi_dbm,
      signalPercent: o.signal_percent,
      lastSeen: o.captured_at,
    }));
}
