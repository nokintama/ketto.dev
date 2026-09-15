package runner

import (
	"bytes"
	"fmt"
	"os/exec"
	"time"
)

type Result struct {
	Output string
	Error  string
	Time   time.Duration
}

func Run(language string, code string) Result {
	start := time.Now()

	cmd := exec.Command("docker", "run", "--rm",
		"--memory=64m",
		"--cpus=0.5",
		fmt.Sprintf("judge-%s:latest", language),
		code,
	)
	var out, errBuf bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &errBuf

	err := cmd.Run()
	elapsed := time.Since(start)

	if err != nil {
		return Result{Error: errBuf.String(), Time: elapsed}

	}
	return Result{Output: out.String(), Time: elapsed}
}
