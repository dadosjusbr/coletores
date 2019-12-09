package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/dadosjusbr/storage"
	"github.com/kelseyhightower/envconfig"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/mongo/readpref"
	"gopkg.in/mgo.v2/bson"
)

type config struct {
	MongoDBURI        string `envconfig:"MONGODB_URI" required:"true"`
	MongoDBName       string `envconfig:"MONGODB_NAME" required:"true"`
	MongoDBCollection string `envconfig:"MONGODB_COLLECTION" required:"true"`
}

func main() {
	var c config
	if err := envconfig.Process("", &c); err != nil {
		log.Fatalf("error loading config values: %q\n", err.Error())
	}
	fmt.Fprintf(os.Stderr, "Loaded prefs:%+v\n", c)
	mgo, err := mongo.NewClient(options.Client().ApplyURI(c.MongoDBURI))
	if err != nil {
		log.Fatalf("error creating mongodb client: %q\n", err.Error())
	}

	ctx, cancelCtx := context.WithTimeout(context.Background(), 10*time.Second)
	if err = mgo.Connect(ctx); err != nil {
		log.Fatalf("error connecting to mongodb: %q\n", err.Error())
	}
	defer cancelCtx()

	// Calling Connect does not block for server discovery. Need to ping.
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	if err = mgo.Ping(ctx, readpref.Primary()); err != nil {
		log.Fatalf("could not find any available mongo instance: %q\n", err.Error())
	}
	fmt.Fprintf(os.Stderr, "Sucessfully connected to mongodb %s\n", c.MongoDBURI)
	defer cancel()

	cur, err := mgo.Database(c.MongoDBName).Collection(c.MongoDBCollection).Find(context.Background(), bson.M{})
	if err != nil {
		log.Fatalf("error querying mongodb:%q", err)
	}
	defer cur.Close(context.Background())
	csvHeaders()
	for cur.Next(context.Background()) {
		var mi storage.AgencyMonthlyInfo
		if err := cur.Decode(&mi); err != nil {
			log.Fatalf("error decoding value from mongodb:%q\n", err)
		}
		err = logAgencyMonthlyInfo(mi)
		if err != nil {
			log.Fatalf("error logging agency: %q", err)
		}
	}
	if err := cur.Err(); err != nil {
		log.Fatalf("error dealing with mongodb cursor:%q\n", err)
	}
}

// csvHeaders prints headers for the csv to stdout
func csvHeaders() {
	fmt.Printf(`"aid", "year", "month",`)
	fmt.Printf(`"reg", "name", "role", "type", "workplace", "active",`)
	fmt.Printf(`"income_total", "wage",`)
	fmt.Printf(`"perks_total", "perks_food", "perks_transportation", "perks_preschool", "perks_health","perks_birthaid","perks_housingaid","perks_subsistence", "perks_others",`)
	fmt.Printf(`"others_total", "others_personalbenefits", "others_eventualbenefits", "others_positionoftrust", "others_daily", "others_gratification", "others_originposition", "others_others",`)
	fmt.Printf(`"discounts_total", "discounts_prevcontribution", "discounts_ceilretention", "discounts_incometax", "discounts_others"`)
	fmt.Println()
}

// logAgencyMonthlyInfo will take a AgencyMonthlyInfo and prints to stdout all the employees as csv lines.
func logAgencyMonthlyInfo(ag storage.AgencyMonthlyInfo) error {
	for _, e := range ag.Employee {
		basicInfo := fmt.Sprintf("%q, %d, %d,", ag.AgencyID, ag.Year, ag.Month)
		empInfo := empInfo(e)
		fmt.Println(basicInfo + empInfo[:len(empInfo)-1])
	}
	return nil
}

// empInfo returns the employee as a csv line.
func empInfo(e storage.Employee) string {
	basicInfo := fmt.Sprintf("%q, %q, %q, %q, %q, %t,", e.Reg, e.Name, e.Role, e.Type, e.Workplace, e.Active)
	income := incomeInfo(e.Income)
	discounts := discountInfo(e.Discounts)
	line := basicInfo + income + discounts
	return line
}

// incomeInfo generates the IncomeDetails as a csv line
func incomeInfo(i *storage.IncomeDetails) string {
	if i == nil {
		return ",,,,,,,,,,,,,,,,,,,,,"
	}
	result := fmt.Sprintf("%.2f,", i.Total) + getFloatValues(i.Wage)
	// Perks
	if i.Perks == nil {
		result += ",,,,,,,,,,"
	} else {
		result += fmt.Sprintf("%.2f,", i.Perks.Total) +
			getFloatValues(i.Perks.Food, i.Perks.Transportation, i.Perks.PreSchool, i.Perks.Health, i.Perks.BirthAid, i.Perks.HousingAid, i.Perks.Subsistence) +
			getMapTotal(i.Perks.Others)
	}
	// Others
	if i.Other == nil {
		result += ",,,,,,,,,"
	} else {
		result += fmt.Sprintf("%.2f,", i.Other.Total) +
			getFloatValues(i.Other.PersonalBenefits, i.Other.EventualBenefits, i.Other.PositionOfTrust, i.Other.Daily, i.Other.Gratification, i.Other.OriginPosition) +
			getMapTotal(i.Other.Others)
	}
	return result
}

// discountInfo generates discount info as a csv line.
func discountInfo(d *storage.Discount) string {
	if d == nil {
		return ",,,,,"
	}
	result := fmt.Sprintf("%.2f,", d.Total) + getFloatValues(d.PrevContribution, d.CeilRetention, d.IncomeTax) + getMapTotal(d.Others)
	return result
}

// getFloatValues takes a list of float pointers and returns them as a string for csv.
func getFloatValues(floats ...*float64) string {
	result := ""
	for _, p := range floats {
		if p == nil {
			result += ","
		} else {
			result += fmt.Sprintf("%.2f,", *p)
		}
	}
	return result
}

// getMapTotal returns sum of map values as a csv field("%.2f,").
func getMapTotal(m map[string]float64) string {
	total := 0.
	for _, v := range m {
		total += v
	}
	return fmt.Sprintf("%.2f,", total)
}
