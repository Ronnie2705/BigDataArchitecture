import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.css']
})
export class AppComponent {
  aboutPopupVisible = false;

  togglePopup(popupId: string): void {
    if (popupId === 'about-popup') {
      this.aboutPopupVisible = !this.aboutPopupVisible;
    }
  }

  togglePopup1(popupId: string): void {
    if (popupId === 'about-popup') {
      this.aboutPopupVisible = !this.aboutPopupVisible;
    }
  }

  togglePopup2(popupId: string): void {
    if (popupId === 'about-popup') {
      this.aboutPopupVisible = !this.aboutPopupVisible;
    }
  }

  togglePopup3(popupId: string): void {
    if (popupId === 'about-popup') {
      this.aboutPopupVisible = !this.aboutPopupVisible;
    }
  }

  togglePopup4(popupId: string): void {
    if (popupId === 'about-popup') {
      this.aboutPopupVisible = !this.aboutPopupVisible;
    }
  }
}
