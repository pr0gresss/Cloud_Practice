# Cloud_Practice

FastAPI service for `Portfolio`, `Artwork`, and `Feedback` management.

## API

- `GET /health`
- `POST /api/portfolios`
- `GET /api/portfolios`
- `GET /api/portfolios/{portfolio_id}`
- `PUT /api/portfolios/{portfolio_id}`
- `DELETE /api/portfolios/{portfolio_id}`
- `POST /api/artworks`
- `GET /api/artworks`
- `GET /api/artworks/{artwork_id}`
- `GET /api/artworks/portfolio/{portfolio_id}`
- `PUT /api/artworks/{artwork_id}`
- `DELETE /api/artworks/{artwork_id}`
- `POST /api/artworks/{artwork_id}/attach-portfolio/{portfolio_id}`
- `POST /api/artworks/{artwork_id}/upload-image`
- `POST /api/feedbacks`
- `GET /api/feedbacks`
- `GET /api/feedbacks/{feedback_id}`
- `GET /api/feedbacks/portfolio/{portfolio_id}`
- `PUT /api/feedbacks/{feedback_id}`
- `DELETE /api/feedbacks/{feedback_id}`
- `POST /api/feedbacks/{feedback_id}/attach-portfolio/{portfolio_id}`

## Notes

- Stateless API nodes support horizontal scaling behind a load balancer.
- Media storage is isolated behind a storage service abstraction, ready for S3 or another object store.
- Feedback creation emits queued events and uses retry tracking for eventual consistency.
- Request and entity-level operations are logged.
