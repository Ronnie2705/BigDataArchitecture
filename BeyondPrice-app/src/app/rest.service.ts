import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class RestService {
  postSignupURL= "http://localhost/apiv1/signup"
  data: any;

  
  constructor(private http:HttpClient, private router: Router) { }
  
  postSignupData(firstName:string,lastName:string,email:string,phoneNumber:string,password:string){
    const data = { firstName: firstName, lastName: lastName, email:email,phoneNumber:phoneNumber,password:password };
    console.log(data)
    // return this.http.post(this.postSignupURL,data).subscribe()
    this.http.post(this.postSignupURL, data).subscribe(response => {
      console.log(response);
      // value= response.
      if(response){
        console.log("Welcome" + firstName);
        this.router.navigate(['/login']);
      }
    });
  }

  postloginURL= "http://localhost/apiv1/login"
  postlogin(email:string,password:string){
    const data = {email:email,password:password };
    console.log(data)
    // return this.http.post(this.postSignupURL,data).subscribe()
    this.http.post(this.postloginURL, data).subscribe(response => {
      console.log(response);
      
      // value= response.
      // if(response.toString()=="SignUp is complete!"){
      //   console.log("Welcome" + firstName);
      // }
    });
  }

  // getProducts(){
    
  //   this.http.get("http://localhost/apiv1/fetchData/Mobiles/45.00/362.17").subscribe(resp=>{
  //     this.data = resp
  //     console.log("jhansi",resp)
  //     return resp
  // }
  //   );
  //   console.log("swaps",this.data)
  //   return this.data
  // }
}
