package status

import "fmt"

// StatusError wraps a code and a error messager
type StatusError struct {
	Err  error
	Code Code
}

// NewStatusError creates a new StatusError
func NewStatusError(code Code, error error) error {
	return &StatusError{
		Err:  error,
		Code: code,
	}
}

func (se *StatusError) Error() string {
	return fmt.Sprintf("error %v , %v", se.Code, se.Err.Error())
}
