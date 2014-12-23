//
//  ParkersRequests.swift
//  ParkingSpot
//
//  Created by Charlie X. Zhou on 11/21/14.
//  Copyright (c) 2014 Charlie X. Zhou. All rights reserved.
//

import Alamofire
import Foundation
import MapKit

let host = "parkers.silvlinings.com"
//let host = "172.16.30.112:8000"
//let host = "127.0.0.1:8000"

let client_id = "test"
let client_secret = "test"
var token_timer: NSTimer?

private let _SingletonASharedInstance = ParkersRequest()

class ParkersRequest {
    
    class var sharedInstance : ParkersRequest {
        return _SingletonASharedInstance
    }
    
    // api router
    enum Router: URLRequestConvertible {
        static let baseURLString = "http://" + host
        static var OAuthToken: String?
        
        case Query([String: AnyObject])
        case PostNotify([String: AnyObject])
        case GetNotify()
        
        var method: Alamofire.Method {
            switch self {
            case .Query:
                return .POST
            case .PostNotify:
                return .GET
            case .GetNotify:
                return .GET
            }
        }
        
        var path: String {
            switch self {
            case .Query:
                return "/query/api/"
            case .PostNotify:
                return "/notifier/post/"
            case .GetNotify:
                return "/notifier/"
            }
        }
        
        // MARK: URLRequestConvertible
        
        var URLRequest: NSURLRequest {
            let URL = NSURL(string: Router.baseURLString)!
            let mutableURLRequest = NSMutableURLRequest(URL: URL.URLByAppendingPathComponent(path))
            mutableURLRequest.HTTPMethod = method.rawValue
            
            if let token = Router.OAuthToken {
                mutableURLRequest.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
            }
            
            switch self {
            case .Query(let parameters):
                return Alamofire.ParameterEncoding.URL.encode(mutableURLRequest, parameters: parameters).0
            case .PostNotify(let parameters):
                return Alamofire.ParameterEncoding.URL.encode(mutableURLRequest, parameters: parameters).0
            default:
                return mutableURLRequest
            }
        }
    }
    
    
    func login(#username:String, password:String, curretView: MainViewController){
        Alamofire.request(.POST, "http://" + host + "/o/token/", parameters: [
            "client_id": client_id,
            "client_secret": client_secret,
            "username": username,
            "password": password,
            "grant_type": "password"
            ])
            .responseJSON { (_, _, JSON, err) in
                if(err != nil){
                    var alert = UIAlertController(title: "Login Failed", message: "The server is down. 😂", preferredStyle: UIAlertControllerStyle.Alert)
                    alert.addAction(UIAlertAction(title: "Retry", style: UIAlertActionStyle.Default, handler: { action in
                        switch action.style {
                            case .Default:
                                self.login(username: username, password: password, curretView: curretView)
                        
                            case .Cancel:
                                println("cancel")
                        
                            case .Destructive:
                                println("destructive")
                            
                        }
                    }))
                   
                    curretView.presentViewController(alert, animated: true, completion: nil)
                }else{
                    Router.OAuthToken = JSON?.valueForKey("access_token") as? String
                }
        }
    }
    
    func query(place:PlaceModel, cb: () -> Void) {
        Alamofire.request(Router.Query(place.payload))
            .responseJSON { (_, _, JSON, _) in
                if(JSON == nil) {
                    return
                }
                place.results = JSON as [AnyObject]
                cb()
        }
    }
    
    func getNotify(dict:AnyObject, cb: ()->Void){
        Alamofire.request(Router.GetNotify())
            .responseJSON { (_, _, JSON, _) in
                if(JSON == nil) {
                    return
                }
                
        }
    }
    
    func postNotify(payload: [String: String], cb: () -> Void) {
        Alamofire.request(Router.PostNotify(payload))
            .responseJSON { (_, _, JSON, _) in
                if(JSON == nil) {
                    return
                }
                cb()
        }
    }

}

