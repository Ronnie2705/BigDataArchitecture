import { Component, OnInit} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.scss']
})
export class TestComponent implements OnInit {

  
  constructor(private route: ActivatedRoute) {
  }
  

  Brand: String;
  Product_Name: String;
  Image_URL: String;
  Amazon_URL: String;
  Ebay_URL: String;

  ngOnInit(): void {
    this.route.queryParams.subscribe((params: any)=> {
      this.Brand = params.Brand
      this.Product_Name = params.Product_Name
      this.Image_URL = params.Image_URL
      this.Amazon_URL = params.Amazon_URL
      this.Ebay_URL = params.Ebay_URL
    })
  }




}
