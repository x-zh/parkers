//
//  DetailViewController.swift
//  ParkingSpot
//
//  Created by Charlie X. Zhou on 12/14/14.
//  Copyright (c) 2014 Charlie X. Zhou. All rights reserved.
//
import UIKit


class DetailViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {
    
    var place: PlaceModel = PlaceModel()
    
    @IBOutlet weak var resultLabel: UILabel!
    @IBOutlet weak var titleLabel: UILabel!
    @IBOutlet weak var backButton: UIButton!
    @IBOutlet weak var optionView: UIView!
    @IBOutlet weak var optionButton: UIButton!
    @IBOutlet weak var timePickerView: UIView!
    @IBOutlet weak var timePickerViewHeight: NSLayoutConstraint!
    @IBOutlet weak var dateTimeLabel: UILabel!
    @IBOutlet weak var timePickerDoneButton: UIButton!
    @IBOutlet weak var timePickerCancelButton: UIButton!
    @IBOutlet weak var datePicker: UIDatePicker!
    @IBOutlet weak var streetTableView: UITableView!
    
    lazy var dateFormatter: NSDateFormatter = {
        let dateFormatter = NSDateFormatter()
        dateFormatter.dateStyle = NSDateFormatterStyle.MediumStyle
        dateFormatter.timeStyle = .ShortStyle
        return dateFormatter
        }()
    
    override func viewDidLoad() {
        place.displayTitleAndDescription(titleLabel, descriptionLabel: resultLabel)
        
        timePickerView.layer.masksToBounds = false
        timePickerView.layer.shadowColor = UIColor.blackColor().CGColor
        timePickerView.layer.shadowOffset = CGSizeMake(10, 10)
        timePickerView.layer.shadowRadius = 12
        timePickerView.layer.shadowOpacity = 0.7
        timePickerViewHeight.constant = 0
        
        streetTableView.delegate = self
        streetTableView.dataSource = self
        streetTableView.reloadData()
        
        dateTimeLabel.text = place.payload["datetime"] == nil ? dateFormatter.stringFromDate(datePicker.date) : place.payload["datetime"]
        
        datePicker.setDate(dateFormatter.dateFromString(dateTimeLabel.text!)!, animated: false)
        
        backButton.addTarget(self, action: "back", forControlEvents: .TouchUpInside)
        optionButton.addTarget(self, action: "openTimePicker", forControlEvents: .TouchUpInside)
        timePickerDoneButton.addTarget(self, action: "doneTimePicker", forControlEvents: .TouchUpInside)
        timePickerCancelButton.addTarget(self, action: "closeTimePicker", forControlEvents: .TouchUpInside)
        super.viewDidLoad()
    }
    
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        if (place.sorted_streets.count > 0) {
            return place.sorted_streets.count + 1
        }
        return 1
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        var cell =  UITableViewCell(style: UITableViewCellStyle.Subtitle, reuseIdentifier: nil)
        if (place.sorted_streets.count > 0) {
            if(indexPath.row == 0){
                cell.textLabel?.text = "Show All"
                cell.detailTextLabel?.text = "Including \(place.results.count) blocks."
            }else{
                let street_name:String = place.sorted_streets[indexPath.row - 1][0].location
                let hours: String = place.sorted_streets[indexPath.row-1][0].getHours()
                cell.textLabel?.text =  street_name
                cell.detailTextLabel?.numberOfLines = 0
                cell.detailTextLabel?.text = "Including \(place.sorted_streets[indexPath.row - 1].count) blocks. \n\(hours)"
            }
        } else {
            cell.textLabel?.text = "Can't find any parking?"
            cell.detailTextLabel?.text = "Change your parking time by clicking OPTIONS."
        }
        return cell
    }
    
    func tableView(tableView: UITableView, heightForRowAtIndexPath indexPath: NSIndexPath) -> CGFloat{
        if (indexPath.row == 0) {
            return 44;
        }
        return 64;
    }
    
    func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        if (place.sorted_streets.count > 0) {
            let mView : MainViewController = (self.presentingViewController as MainViewController)
            if(indexPath.row == 0){
                // show all
                place.displayAllStreetsOnMap(mView.mapView)
            }
            else {
                // show that street
                place.displayStreetOnMap(place.sorted_streets[indexPath.row - 1][0].location,
                    mapView: mView.mapView)
            }
            dismissViewControllerAnimated(true, completion: {})
        }
        else {
            openTimePicker()
        }
    }
    
    @IBAction func back(){
        dismissViewControllerAnimated(true, completion: {})
    }
    @IBAction func openTimePicker(){
        self.timePickerViewHeight.constant = 252.0
    }
    @IBAction func closeTimePicker(){
        self.timePickerViewHeight.constant = 0
    }
    @IBAction func doneTimePicker(){
        self.timePickerViewHeight.constant = 0
        place.payload["datetime"] = dateFormatter.stringFromDate(datePicker.date)
        place.query({
            self.streetTableView.reloadData()
            let mView : MainViewController = (self.presentingViewController as MainViewController)
            self.dateTimeLabel.text = self.place.payload["datetime"]
            // self.place.displayAllStreetsOnMap(mView.mapView)
            self.place.displayTitleAndDescription(mView.placeTitle, descriptionLabel: mView.placeDescription)
            self.place.displayTitleAndDescription(self.titleLabel, descriptionLabel: self.resultLabel)
        })
    }
}