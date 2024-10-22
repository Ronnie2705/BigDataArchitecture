import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { delay } from 'rxjs';
import { query } from '@angular/animations';

export interface Response {
  message: string
}

@Injectable({
  providedIn: 'root'
})



export class RestService {
  postSignupURL= "/apiv1/signup"
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
 
  postloginURL= "/apiv1/login"
  postlogin(email:string,password:string){
    const data = {email:email,password:password };
    // console.log(data)
    
    // return this.http.post(this.postSignupURL,data).subscribe()
    this.http.post<Response>(this.postloginURL, data).subscribe(res => {
      // console.log("value1",res) ;
      console.log("Message:",res.message);
      if(res.message=="Incorrect Email or Password" || res.message==undefined){
        alert("Incorrect Email or Password");
      }
      else{
        console.log("Welcome to our portal");
        this.router.navigate(['/userDash']);
      }
     
      
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
