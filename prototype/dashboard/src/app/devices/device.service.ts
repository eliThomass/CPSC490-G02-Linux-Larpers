import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, map } from 'rxjs';

import { DeviceSummary, Observation, summarizeDevices } from './device-summary';

@Injectable({ providedIn: 'root' })
export class DeviceService {
  private readonly http = inject(HttpClient);

  /**
   * Detected devices with their most recent observation.
   * Built from `GET /observations` until the device list endpoint (#139) exists.
   */
  getDevices(): Observable<DeviceSummary[]> {
    return this.http.get<Observation[]>('/observations').pipe(map(summarizeDevices));
  }
}
