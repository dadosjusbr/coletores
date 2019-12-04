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
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	if err = mgo.Connect(ctx); err != nil {
		log.Fatalf("error connecting to mongodb: %q\n", err.Error())
	}
	// Calling Connect does not block for server discovery. Need to ping.
	ctx, _ = context.WithTimeout(context.Background(), 30*time.Second)
	if err = mgo.Ping(ctx, readpref.Primary()); err != nil {
		log.Fatalf("could not find any available mongo instance: %q\n", err.Error())
	}
	fmt.Fprintf(os.Stderr, "Sucessfully connected to mongodb %s\n", c.MongoDBURI)

	cur, err := mgo.Database(c.MongoDBName).Collection(c.MongoDBCollection).Find(context.Background(), bson.M{})
	if err != nil {
		log.Fatalf("error querying mongodb:%q", err)
	}
	defer cur.Close(context.Background())
	for cur.Next(context.Background()) {
		var mi storage.AgencyMonthlyInfo
		if err := cur.Decode(&mi); err != nil {
			log.Fatalf("error decoding value from mongodb:%q\n", err)
		}
		// TODO: Para cada registro, transformar em CSV e imprimir na saída padrão.
	}
	if err := cur.Err(); err != nil {
		log.Fatalf("error dealing with mongodb cursor:%q\n", err)
	}
}
