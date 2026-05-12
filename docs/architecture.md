# Architecture

Showing Follow-up Orchestrator treats post-showing conversion as a sequencing problem.

## Inputs

- Hours since showing
- Interest signal
- Price fit
- Disclosure request
- Second-showing request
- Financing readiness
- Objection count
- Preferred communication channel

## Core idea

Most agents either over-message or wait too long. This repo keeps three decisions visible:

- how hot the buyer actually is
- how urgent the follow-up should be
- what cadence and channel make sense for the next contact

## Outputs

- Follow-up queue
- Cadence board
- Buyer-intent evidence view
- API payloads for CRMs and reminder systems
