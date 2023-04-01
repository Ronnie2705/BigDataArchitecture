import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-prod-compare',
  templateUrl: './prod-compare.component.html',
  styleUrls: ['./prod-compare.component.scss']
})
export class ProdCompareComponent implements OnInit{
  constructor(private route: ActivatedRoute,private router: Router,private http:HttpClient) { }
  shoeURL:string = "../assets/images/shoe.jpg"

  Brand: String;
  Product_Name: String;
  Image_URL: String;
  Amazon_URL: String;
  Ebay_URL: String;


  price: object;
  public isLoading: boolean = false;


  ngOnInit(): void {
    this.isLoading = true;
    this.route.queryParams.subscribe((params: any)=> {
      this.Brand = params.Brand
      this.Product_Name = params.Product_Name
      this.Image_URL = params.Image_URL
      this.Amazon_URL = params.Amazon_URL
      this.Ebay_URL = params.Ebay_URL
    });


    
    const URL_data = {Amazon_URL:this.Amazon_URL,Ebay_URL:this.Ebay_URL };
    const compare_url = 'http://localhost/apiv1/compareProducts';

    this.http.post(compare_url,URL_data).subscribe(resp=>{
      this.isLoading = false;
      this.price  = resp
      console.log("price",resp)
      return resp
  }, err => { this.isLoading = false; }
    );




  }


}
