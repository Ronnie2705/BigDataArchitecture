import { Component } from '@angular/core';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.scss']
})
export class AboutComponent {
  show = {
    about: false,
    howItWorks: false,
    why: false,
    faqs: false,
    privacyPolicy: false
  };

  togglePopup(popup: 'about'): void {
    this.show[popup] = !this.show[popup];
  }

  togglePopup1(popup1: 'howItWorks'): void {
    this.show[popup1] = !this.show[popup1];
  }

  togglePopup2(popup2: 'why'): void {
    this.show[popup2] = !this.show[popup2];
  }

  togglePopup3(popup3: 'faqs'): void {
    this.show[popup3] = !this.show[popup3];
  }

  togglePopup4(popup4: 'privacyPolicy'): void {
    this.show[popup4] = !this.show[popup4];
  }
}
