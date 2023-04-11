import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-products',
  templateUrl: './products.component.html',
  styleUrls: ['./products.component.scss']
})
export class ProductsComponent  implements OnInit  {
  data_URL: string;
  products_data: Object;
  product_data: object;
  public isLoading: boolean = false;

  constructor(private route: ActivatedRoute,private router: Router,private http:HttpClient){
}
  ngOnInit(): void {
    this.isLoading = true;
    this.route.queryParams.subscribe((params: any)=> {
      this.data_URL = params.url
    })

    console.log(this.data_URL)
    
    this.http.get("/apiv1/fetchData/"+this.data_URL).subscribe(resp=>{
      this.isLoading = false;
      this.products_data = resp
      console.log("jhansi",resp)
      return resp
  }, err => { this.isLoading = false; }
    );
  }



gotoCompareProducts(product){
  console.log(product)

  this.router.navigate(['/compareProducts'],{queryParams:{Brand:product.Brand,Product_Name:product.Product_Name,Image_URL:product.Image_URL,price:product.price,Amazon_URL:product.Amazon_URL,Ebay_URL:product.Ebay_URL}})

}
}
