//
//  NotifyViewController.swift
//  ParkingSpot
//
//  Created by Charlie X. Zhou on 12/15/14.
//  Copyright (c) 2014 Charlie X. Zhou. All rights reserved.
//
import UIKit


class NotifyViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {
    
    var objects = [
        "70th Street, Brooklyn",
        "107-23 Lefferts Boulevard, Queens",
        "469 46th Street, Brooklyn",
        "New York University, 60 Washington Square",
        "6 Metrotech Center, Brooklyn"
    ]
    @IBOutlet weak var shareResultTableView: UITableView!
    
    @IBAction func Close (CloseButton: UIButton!) {
        // Go back to the previous screen
        dismissViewControllerAnimated(true, completion: {})
    }
    
    @IBAction func Share(ShareButton: UIButton!) {
        // Send to the server
    }
    
    override func viewDidLoad() {
        shareResultTableView.delegate = self
        shareResultTableView.dataSource = self
        super.viewDidLoad()
    }
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return objects.count
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        var cell =  UITableViewCell(style: UITableViewCellStyle.Subtitle, reuseIdentifier: nil)
        cell.textLabel?.text = objects[indexPath.row]
        return cell
    }
}