package worker

import (
	"log"
)

type Pool struct {
	workers int
	jobs    chan Job
}

type Job struct {
	ID       string
	Language string
	Code     string
}

func NewPool(workers int) *Pool {
	return &Pool{workers: workers,
		jobs: make(chan Job, 100),
	}
}

func (p *Pool) Start() {
	for i := 0; i < p.workers; i++ {
		go p.worker(i)
	}
	log.Printf("Worker pool started with %d workers", p.workers)
}

func (p *Pool) Submit(job Job) {
	p.jobs <- job
}

func (p *Pool) worker(id int) {
	for job := range p.jobs {
		log.Printf("Worker %d processing job %s", id, job.ID)
	}
}
