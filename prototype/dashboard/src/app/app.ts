import { Component } from '@angular/core';

import { DeviceList } from './devices/device-list';

@Component({
  imports: [DeviceList],
  selector: 'app-root',
  styleUrl: './app.css',
  templateUrl: './app.html',
})
export class App {}
