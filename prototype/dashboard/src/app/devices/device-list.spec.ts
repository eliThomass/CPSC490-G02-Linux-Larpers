import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DeviceList } from './device-list';
import { Observation, summarizeDevices } from './device-summary';

const SCANNER = '11111111-1111-1111-1111-111111111111';
const SESSION = '22222222-2222-2222-2222-222222222222';

function observation(overrides: Partial<Observation>): Observation {
  return {
    observation_id: crypto.randomUUID(),
    scanner_id: SCANNER,
    session_id: SESSION,
    device_id: null,
    captured_at: '2026-11-24T18:00:00Z',
    received_at: '2026-11-24T18:00:01Z',
    protocol: 'wifi',
    observed_address: null,
    address_type: null,
    rssi_dbm: null,
    signal_percent: null,
    metadata: {},
    ...overrides,
  };
}

// The same known test dataset loaded into the local database for #140.
const DATASET: Observation[] = [
  observation({ device_id: 'dev-ring-0002', captured_at: '2026-11-24T18:02:00Z', protocol: 'wifi', rssi_dbm: -55, signal_percent: 74 }),
  observation({ device_id: 'dev-meta-0001', captured_at: '2026-11-24T18:05:00Z', protocol: 'bluetooth', rssi_dbm: -71 }),
  observation({ device_id: 'dev-anon-0003', captured_at: '2026-11-24T18:10:00Z', protocol: 'wifi' }),
  observation({ device_id: null, captured_at: '2026-11-24T18:12:00Z', protocol: 'bluetooth', rssi_dbm: -90 }),
  observation({ device_id: 'dev-ring-0002', captured_at: '2026-11-24T18:15:00Z', protocol: 'wifi', rssi_dbm: -49, signal_percent: 82 }),
  observation({ device_id: 'dev-meta-0001', captured_at: '2026-11-24T18:20:00Z', protocol: 'bluetooth', rssi_dbm: -58 }),
];

describe('summarizeDevices', () => {
  it('keeps one row per device, using its most recent observation, newest first', () => {
    const rows = summarizeDevices(DATASET);
    expect(rows.map((r) => [r.deviceId, r.lastSeen, r.rssiDbm])).toEqual([
      ['dev-meta-0001', '2026-11-24T18:20:00Z', -58],
      ['dev-ring-0002', '2026-11-24T18:15:00Z', -49],
      ['dev-anon-0003', '2026-11-24T18:10:00Z', null],
    ]);
  });

  it('skips observations that are not linked to a device', () => {
    const rows = summarizeDevices([observation({ device_id: null, rssi_dbm: -90 })]);
    expect(rows).toEqual([]);
  });
});

describe('DeviceList', () => {
  let fixture: ComponentFixture<DeviceList>;
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DeviceList],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();
    fixture = TestBed.createComponent(DeviceList);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  async function respondWith(body: Observation[]): Promise<HTMLElement> {
    fixture.detectChanges();
    http.expectOne('/observations').flush(body);
    await fixture.whenStable();
    fixture.detectChanges();
    return fixture.nativeElement as HTMLElement;
  }

  it('shows identification, protocol, signal strength and last-seen time for each device', async () => {
    const page = await respondWith(DATASET);
    const rows = [...page.querySelectorAll('tbody tr')].map((tr) =>
      [...tr.querySelectorAll('td')].map((td) => td.textContent?.trim()),
    );
    expect(rows).toEqual([
      ['Unknown device (…0001)', 'Bluetooth', '-58 dBm', '2026-11-24 18:20:00'],
      ['Unknown device (…0002)', 'Wi-Fi', '-49 dBm (82%)', '2026-11-24 18:15:00'],
      ['Unknown device (…0003)', 'Wi-Fi', 'Unavailable', '2026-11-24 18:10:00'],
    ]);
  });

  it('says no devices were detected instead of showing an empty table', async () => {
    const page = await respondWith([]);
    expect(page.querySelector('table')).toBeNull();
    expect(page.querySelector('.empty')?.textContent).toContain('No devices detected yet.');
  });

  it('shows an error message when the backend cannot be reached', async () => {
    fixture.detectChanges();
    http.expectOne('/observations').flush('down', { status: 503, statusText: 'Service Unavailable' });
    await fixture.whenStable();
    fixture.detectChanges();
    const page = fixture.nativeElement as HTMLElement;
    expect(page.querySelector('.error')?.textContent).toContain('Could not load devices');
  });
});
