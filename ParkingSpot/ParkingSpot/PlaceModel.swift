//
//  PlaceModel.swift
//  ParkingSpot
//
//  Created by Charlie X. Zhou on 12/14/14.
//  Copyright (c) 2014 Charlie X. Zhou. All rights reserved.
//

import Foundation
import MapKit

class Street {
    var location : String = ""
    var from: String = ""
    var to: String = ""
    var from1: Double = 0
    var from2: Double = 0
    var to1: Double = 0
    var to2: Double = 0
    var side: String = ""
    var days: [Int] = []
    var hourFrom: String = ""
    var hourTo: String = ""
    
    func getHours() -> String {
        return "Sanitation Hour: \(hourFrom) To \(hourTo)"
    }
    func getDescription() -> String {
        return "\(self.location) From \(from) To \(to)"
    }
}

class PlaceModel {
    var title: String = ""
    var results: [AnyObject] = []
    var streets: [String: [Street]] = [:]
    var sorted_streets: [[Street]] = []
    var payload: [String: String] = [:]
    
    func query(cb:()->Void) {
        ParkersRequest.sharedInstance.query(self, {
            self.refreshStreets()
            cb()
        })
    }
    
    func getDescription() -> String {
        var dt = ""
        if payload["datetime"] != nil {
            dt = "@ " + payload["datetime"]!
        }
        return "Found \(self.streets.count) streets \(dt)"
    }
    
    func displayTitleAndDescription(titleLabel: UILabel, descriptionLabel: UILabel){
        titleLabel.text = self.title
        descriptionLabel.text = self.getDescription()
    }
    
    func refreshStreets() {
        streets = [:]
        for line: AnyObject in self.results as [AnyObject]{
            var s = Street()
            s.from = line.valueForKey("from")?[0] as String
            s.from1 = NSString(string: line.valueForKey("from")?[1] as String).doubleValue
            s.from2 = NSString(string: line.valueForKey("from")?[2] as String).doubleValue
            s.to = line.valueForKey("to")?[0] as String
            s.to1 = NSString(string: line.valueForKey("to")?[1] as String).doubleValue
            s.to2 = NSString(string: line.valueForKey("to")?[2] as String).doubleValue
            s.location = line.valueForKey("location") as String
            s.side = line.valueForKey("side") as String
            let dt:AnyObject = line.valueForKey("datetime")!
            s.days = dt.valueForKey("days") as [Int]
            s.hourFrom = dt.valueForKey("hours")?[0] as String
            s.hourTo = dt.valueForKey("hours")?[1] as String
            if(streets.indexForKey(s.location) == nil){
                streets[s.location] = []
            }
            streets[s.location]?.append(s)
        }
        sorted_streets = [[Street]](streets.values)
        sorted_streets.sort({$0.count > $1.count})
    }
    
    func displayStreetOnMap(streetname: String, mapView: MKMapView){
        mapView.removeOverlays(mapView.overlays)
        _displayStreetOnMap(streetname, mapView: mapView)
    }
    
    func displayAllStreetsOnMap(mapView: MKMapView){
        if(self.results.count == 0){
            return
        }
        mapView.removeOverlays(mapView.overlays)
        for sn:String in self.streets.keys {
            _displayStreetOnMap(sn, mapView: mapView)
        }
    }
    
    func _displayStreetOnMap(streetname: String, mapView: MKMapView){
        let ss:[Street] = streets[streetname]!
        for s:Street in ss {
            let w = s.from1 - s.to1
            let h = s.from2 - s.to2
            if(w > 0.005 || w < -0.005 || h > 0.005 || h < -0.005){
                continue
            }
            var mb = [
                CLLocationCoordinate2D(
                    latitude: s.from1,
                    longitude: s.from2
                ),
                CLLocationCoordinate2D(
                    latitude: s.to1,
                    longitude: s.to2
                )
            ]
            var polyline = MKPolyline(coordinates: &mb, count: 2)
            mapView.addOverlay(polyline)
        }
    }
    
    
}