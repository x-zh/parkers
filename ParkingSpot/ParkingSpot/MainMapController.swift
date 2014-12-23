//
//  MainViewController.swift
//  ParkingSpot
//
//  Created by Charlie X. Zhou on 11/15/14.
//  Copyright (c) 2014 Charlie X. Zhou. All rights reserved.
//
import CoreLocation
import UIKit
import MapKit



class MainViewController: UIViewController, UISearchBarDelegate, CLLocationManagerDelegate, MKMapViewDelegate, UITableViewDelegate, UITableViewDataSource {
    
    var manager:CLLocationManager!
    var searchResponse: [AnyObject] = []
    var place:PlaceModel = PlaceModel()
    var currentLocation:CLLocation!
    
    @IBAction func gotoCurrent(sender: AnyObject) {
        show_neighbor("Current Location", userlocation: currentLocation)
        
    }
    @IBOutlet weak var mapView: MKMapView!
    @IBOutlet weak var searchResult: UITableView!
    @IBOutlet weak var searchBar: UISearchBar!
    @IBOutlet weak var placeTitle: UILabel!
    @IBOutlet weak var placeTitleView: UIView!
    @IBOutlet weak var placeDescription: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // login first
        
        //temp
        let username = "johnqiao"
        let password = "0zyr72VWip40"
//        let password = "123"
        ParkersRequest.sharedInstance.login(username: username, password: password, curretView:self)
        
        // user location
        manager = CLLocationManager()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyBest
        manager.distanceFilter = 10
        manager.requestAlwaysAuthorization()
        manager.startUpdatingLocation()
        mapView.delegate = self
        mapView.showsUserLocation = true
        
        // ui
        searchBar.delegate = self
        searchResult.delegate = self
        searchResult.dataSource = self
        searchResult.hidden = true
        
        placeTitleView.hidden = true
        placeTitleView.layer.masksToBounds = false
        placeTitleView.layer.shadowColor = UIColor.blackColor().CGColor
        placeTitleView.layer.shadowOffset = CGSizeMake(10, 10);
        placeTitleView.layer.shadowRadius = 10;
        placeTitleView.layer.shadowOpacity = 0.7;
    }
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.searchResponse.count
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        var cell =  UITableViewCell(style: .Default, reuseIdentifier: nil)
        cell.textLabel?.text = (self.searchResponse[indexPath.row] as MKMapItem).name
        return cell
    }
    
    func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        let mapItem = self.searchResponse[indexPath.row] as MKMapItem
        let searchLocation = CLLocation(latitude: mapItem.placemark.coordinate.latitude,
            longitude: mapItem.placemark.coordinate.longitude)
        show_neighbor(mapItem.name, userlocation:searchLocation)
        
        // remove previous pin
        let annotation = MKPointAnnotation()
        mapView.removeAnnotations(mapView.annotations)
        // put pin
        annotation.setCoordinate(searchLocation.coordinate)
        mapView.addAnnotation(annotation)
        // search result
        searchResult.hidden = true
    }
    
    func searchBarSearchButtonClicked(searchBar: UISearchBar) {
        var request = MKLocalSearchRequest()
        request.naturalLanguageQuery = searchBar.text
        request.region = self.mapView.region //need to define region later
        var search:MKLocalSearch = MKLocalSearch.init(request:request)
        search.startWithCompletionHandler {
            (response:MKLocalSearchResponse!, error:NSError!) in
            if (error == nil) {
                self.searchResponse = []
                for item in response.mapItems {
                    self.searchResponse.append(item)
                }
                // ui
                self.placeTitleView.hidden = true
                self.searchResult.hidden = false
                self.searchResult.reloadData()
            }
        }
    }
    
    func locationManager(manager:CLLocationManager, didUpdateLocations locations:[AnyObject]) {
        currentLocation = locations[0] as CLLocation
        show_neighbor("Current Location", userlocation: currentLocation)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func mapView(mapView: MKMapView!, rendererForOverlay overlay: MKOverlay!) -> MKOverlayRenderer! {
        if overlay is MKPolyline {
            var polylineRenderer = MKPolylineRenderer(overlay: overlay)
            polylineRenderer.strokeColor = UIColor(red: 142/255.0, green: 68/255.0, blue: 173/255.0, alpha: 1)
            polylineRenderer.lineWidth = 4
            return polylineRenderer
        }
        return nil
    }
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject!) {
        if (segue.identifier == "TheDetailSegue") {
            //get a reference to the destination view controller
            let destinationVC:DetailViewController = segue.destinationViewController as DetailViewController
            destinationVC.place = self.place
        }
    }
    
    func show_neighbor (title:String, userlocation:CLLocation) {
        // zoom in
        let span = MKCoordinateSpanMake(0.05, 0.05)
        let region = MKCoordinateRegion(center: userlocation.coordinate, span: span)
        mapView.setRegion(region, animated: true)
        mapView.regionThatFits(region)
        
        // placeTitleView
        place.title = title
        place.payload = [
            "latitude": NSString(format:"%.6f", userlocation.coordinate.latitude as Double),
            "longitude": NSString(format:"%.6f", userlocation.coordinate.longitude as Double)
        ]
        place.query({
            self.updatePlaceOnUI()
        })
    }
    
    func updatePlaceOnUI() {
        placeTitleView.hidden = false
        place.displayTitleAndDescription(placeTitle, descriptionLabel: placeDescription)
        place.displayAllStreetsOnMap(mapView)
    }
    
    
}

