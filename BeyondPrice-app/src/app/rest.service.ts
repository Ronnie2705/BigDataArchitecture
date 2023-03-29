import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class RestService {
  postSignupURL= "http://localhost//apiv1/signin"

  constructor(private http:HttpClient) { }
  postSignupData(firstName:string,lastName:string,email:string,phoneNumber:string,password:string){
    const data = { firstName: firstName, lastName: lastName, email:email,phoneNumber:phoneNumber,password:password };
    console.log(data)
    // return this.http.post(this.postSignupURL,data).subscribe()
    this.http.post(this.postSignupURL, data).subscribe(response => {
      if (response['success']) {
        // TODO: Redirect to authenticated page
      } else {
        alert('Invalid username or password');
      }
    });
  }
}
