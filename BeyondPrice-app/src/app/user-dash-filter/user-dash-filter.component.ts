import { Component } from '@angular/core';

@Component({
  selector: 'app-user-dash-filter',
  templateUrl: './user-dash-filter.component.html',
  styleUrls: ['./user-dash-filter.component.scss']
})
export class UserDashFilterComponent {
  shoesURL:string = "../assets/images/shoes.png"
  bagURL:string = "../assets/images/bag.png"
  mobileURL:string = "../assets/images/phone.png"
  laptopURL:string = "../assets/images/laptop.png"

  // onSelected(value: string){
  //   console.log("SIMRIN",value)
  // }

  valueFromSelect;
  onSelected(){
    console.log("SIMRIN",this.valueFromSelect)
  }

}


