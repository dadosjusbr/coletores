package status

// StatusError wraps a code and a error messager
type StatusError struct {
	Message string
	Code    Code
}

// NewStatusError creates a new StatusError
func NewStatusError(code Code, message string) *StatusError {
	return &StatusError{
		Message: message,
		Code:    code,
	}
}
