import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-products',
  templateUrl: './products.component.html',
  styleUrls: ['./products.component.scss']
})
export class ProductsComponent {
  products_data: Object;
  product_data: object;

  constructor(private router: Router,private http:HttpClient){
    console.log("in constructor")
  this.http.get("http://localhost/apiv1/fetchData/Mobiles/45.00/362.17").subscribe(resp=>{
      this.products_data = resp
      console.log("jhansi",resp)
      return resp
  }
    );
}



gotoCompareProducts(product){
  console.log(product)

  this.router.navigate(['/test'],{queryParams:{Brand:product.Brand,Product_Name:product.Product_Name,Image_URL:product.Image_URL,price:product.price,Amazon_URL:product.Amazon_URL,Ebay_URL:product.Ebay_URL}})

}
}
