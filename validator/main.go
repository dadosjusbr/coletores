package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"

	"github.com/dadosjusbr/coletores"
	"github.com/dadosjusbr/coletores/status"
	"github.com/frictionlessdata/datapackage-go/datapackage"
	"github.com/frictionlessdata/tableschema-go/csv"
)

const (
	resourceName = "data" // hardcoded in datapackage_descriptor.json
)

func main() {
	// Reading input.
	in, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		err := status.NewError(status.InvalidInput, fmt.Errorf("Error reading execution result from stdin: %q", err))
		status.ExitFromError(err)
	}
	var er coletores.ExecutionResult
	if err := json.Unmarshal(in, &er); err != nil {
		err := status.NewError(status.InvalidInput, fmt.Errorf("Error unmarshalling execution result: %q", err))
		status.ExitFromError(err)
	}

	// Loading and validating package.
	pkg, err := datapackage.Load(er.Pr.Package)
	if err != nil {
		err = status.NewError(status.DataUnavailable, fmt.Errorf("Error loading datapackage (%s):%q", er.Pr.Package, err))
		status.ExitFromError(err)
	}
	sch, err := pkg.GetResource(resourceName).GetSchema()
	if err != nil {
		err = status.NewError(status.DataUnavailable, fmt.Errorf("Error getting schema from data package resource (%s | %s):%q", er.Pr.Package, resourceName, err))
		status.ExitFromError(err)
	}
	if err := sch.Validate(); err != nil {
		err = status.NewError(status.InvalidInput, fmt.Errorf("Error validating schema (%s):%q", er.Pr.Package, err))
		status.ExitFromError(err)
	}
	var items []coletores.MonthlyPayrollItem
	if err := pkg.GetResource(resourceName).Cast(&items, csv.LoadHeaders()); err != nil {
		err = status.NewError(status.InvalidInput, fmt.Errorf("Error validating datapackage (%s):%q", er.Pr.Package, err))
		status.ExitFromError(err)
	}

	// Printing output.
	out, err := json.MarshalIndent(er, "", "  ")
	if err != nil {
		err = status.NewError(status.OutputError, fmt.Errorf("Error marshaling output:%q", err))
		status.ExitFromError(err)
	}
	fmt.Print(string(out))
}
