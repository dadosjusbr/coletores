package status

import "fmt"

// Error wraps a code and a error messager
type Error struct {
	Err  error
	Code Code
}

// NewError creates a new StatusError
func NewError(code Code, error error) error {
	return &Error{
		Err:  error,
		Code: code,
	}
}

func (se *Error) Error() string {
	return fmt.Sprintf("error %v , %v", se.Code, se.Err.Error())
}
