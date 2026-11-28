import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';

import { DeviceService } from './device.service';
import { DeviceSummary } from './device-summary';

type LoadState = 'loading' | 'loaded' | 'error';

@Component({
  selector: 'app-device-list',
  imports: [DatePipe],
  templateUrl: './device-list.html',
  styleUrl: './device-list.css',
})
export class DeviceList implements OnInit {
  private readonly deviceService = inject(DeviceService);

  protected readonly devices = signal<DeviceSummary[]>([]);
  protected readonly state = signal<LoadState>('loading');

  ngOnInit(): void {
    this.deviceService.getDevices().subscribe({
      next: (devices) => {
        this.devices.set(devices);
        this.state.set('loaded');
      },
      error: () => this.state.set('error'),
    });
  }

  protected identification(device: DeviceSummary): string {
    return device.displayName ?? `Unknown device (…${device.deviceId.slice(-4)})`;
  }

  protected protocolLabel(protocol: string): string {
    if (protocol === 'wifi') return 'Wi-Fi';
    if (protocol === 'bluetooth') return 'Bluetooth';
    return protocol;
  }

  protected signalStrength(device: DeviceSummary): string {
    if (device.rssiDbm === null) return 'Unavailable';
    const percent = device.signalPercent === null ? '' : ` (${device.signalPercent}%)`;
    return `${device.rssiDbm} dBm${percent}`;
  }
}
