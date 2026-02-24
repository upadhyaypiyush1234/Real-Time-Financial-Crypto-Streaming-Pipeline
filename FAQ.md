# Frequently Asked Questions (FAQ)

## General Questions

### Q: Is this really 100% free?
**A:** Yes! All services used have generous free tiers:
- Upstash Kafka: 10,000 messages/day free
- Neon PostgreSQL: 0.5 GB storage free
- Streamlit Cloud: Unlimited public apps
- GitHub Actions: 2,000 minutes/month free
- Binance API: Free public WebSocket

No credit card required for any service.

### Q: How long does setup take?
**A:** 
- Account creation: 10 minutes
- Local setup: 5 minutes
- Testing: 10 minutes
- Deployment: 15 minutes
- **Total: ~40 minutes**

### Q: Do I need prior experience with Kafka?
**A:** No! This project is designed to teach you Kafka while building something real. The code includes extensive comments explaining concepts.

### Q: Can I use this for my portfolio?
**A:** Absolutely! That's what it's designed for. It demonstrates production-ready skills that employers value.

## Technical Questions

### Q: Why Kafka instead of direct database writes?
**A:** Kafka provides:
- **Buffering**: If consumer goes down, no data is lost
- **Replay**: Can reprocess historical data
- **Decoupling**: Producer and consumer are independent
- **Scalability**: Easy to add more consumers
- **Industry standard**: Used by Netflix, Uber, LinkedIn

### Q: How much data will this generate?
**A:** Approximately:
- BTC+ETH: ~100-200 trades/second
- ~10-20 MB/day in database
- Well within free tier limits

### Q: What happens if a component fails?
**A:**
- **Producer fails**: Kafka buffers messages, producer auto-reconnects
- **Consumer fails**: Kafka retains messages, consumer resumes from last offset
- **Database fails**: Consumer retries with exponential backoff
- **Kafka fails**: Upstash handles replication and failover

### Q: Can I add more cryptocurrencies?
**A:** Yes! Edit `.env`:
```env
SYMBOLS=BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,ADAUSDT
```
Restart producer and consumer.

### Q: How do I change the whale threshold?
**A:** Edit `.env`:
```env
WHALE_THRESHOLD=50000  # Alert on trades >$50k
```
Restart consumer.

### Q: Can I use a different exchange?
**A:** Yes, but you'll need to modify the producer to use that exchange's WebSocket API. Binance is used because it's free and has excellent documentation.

## Deployment Questions

### Q: Why use GitHub Actions instead of a server?
**A:** 
- **Free**: 2,000 minutes/month
- **No maintenance**: GitHub manages infrastructure
- **CI/CD**: Automatic deployment on push
- **Learning**: Demonstrates DevOps skills

**Note**: GitHub Actions has a 6-hour timeout. For 24/7 operation, consider Railway, Render, or running locally.

### Q: Can I deploy this to AWS/GCP/Azure?
**A:** Yes! The code is cloud-agnostic. You can:
- Use AWS ECS/Fargate for containers
- Use GCP Cloud Run for serverless
- Use Azure Container Instances
- Keep using Upstash and Neon (they work with any cloud)

### Q: How do I run this 24/7 for free?
**A:** Options:
1. **Old laptop/Raspberry Pi**: Run locally at home
2. **Railway**: Free tier with 500 hours/month
3. **Render**: Free tier with some limitations
4. **Oracle Cloud**: Always-free tier VMs
5. **GitHub Actions**: Run in 6-hour chunks

### Q: Can I make the dashboard private?
**A:** Yes! Streamlit supports authentication:
```python
# Add to dashboard.py
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(...)
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Show dashboard
```

## Data Questions

### Q: How long is data retained?
**A:** 
- **Kafka**: 7 days (configurable in Upstash)
- **Database**: Forever (until you delete it)
- **Free tier**: 0.5 GB (~50M trades)

### Q: How do I delete old data?
**A:**
```sql
DELETE FROM trades WHERE trade_time < NOW() - INTERVAL '30 days';
```

### Q: Can I export data?
**A:**
```bash
psql $DATABASE_URL -c "COPY (SELECT * FROM trades) TO STDOUT WITH CSV HEADER" > trades.csv
```

### Q: What if I hit the free tier limits?
**A:**
- **Upstash**: Reduce symbols or upgrade ($10/month)
- **Neon**: Delete old data or upgrade ($19/month)
- **GitHub Actions**: Use alternative deployment
- **Streamlit**: No limits on free tier

## Performance Questions

### Q: How fast is the pipeline?
**A:**
- **Ingestion**: <10ms per trade
- **Processing**: ~50ms per trade
- **End-to-end**: <1 second from trade to dashboard
- **Throughput**: 1,000+ trades/second

### Q: Can this handle more data?
**A:** Yes! Current bottlenecks and solutions:
- **Database writes**: Batch inserts (10x faster)
- **Consumer processing**: Add more consumer instances
- **Kafka throughput**: Increase partitions
- **Dashboard queries**: Add caching layer

### Q: Why is the dashboard slow?
**A:** Possible causes:
- **Too much data**: Add time-based filtering
- **Slow queries**: Check database indexes
- **Network latency**: Use closer database region
- **Streamlit limits**: Optimize query frequency

## Development Questions

### Q: How do I add tests?
**A:** Add to `tests/`:
```python
def test_my_feature():
    # Your test here
    assert True
```
Run: `pytest tests/ -v`

### Q: How do I add a new feature?
**A:**
1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes
3. Add tests
4. Run tests: `make test`
5. Format code: `make format`
6. Commit and push
7. Create pull request

### Q: How do I debug issues?
**A:**
1. Check logs: `tail -f logs/producer.log`
2. Test connections: See COMMANDS.md
3. Run validation: `python validate.py`
4. Check Upstash/Neon consoles
5. Review GitHub Actions logs

### Q: Can I use this with Docker?
**A:** Yes! Docker files are included:
```bash
docker-compose up -d
```

## Interview Questions

### Q: What would you improve in this project?
**A:** Great interview question! Possible answers:
- Add machine learning for price prediction
- Implement real-time alerting (email/SMS)
- Add authentication and user accounts
- Implement data retention policies
- Add more technical indicators
- Create REST API for external access
- Add comprehensive monitoring/alerting
- Implement A/B testing framework

### Q: How would you scale this to 1M trades/second?
**A:**
1. **Kafka**: Increase partitions to 10+
2. **Consumers**: Deploy 10+ consumer instances
3. **Database**: Shard by symbol, use TimescaleDB
4. **Caching**: Add Redis for hot data
5. **Load balancing**: Use Kubernetes for orchestration
6. **Monitoring**: Add Datadog/New Relic

### Q: What are the security concerns?
**A:**
- **Credentials**: Use secrets management (AWS Secrets Manager)
- **Network**: Use VPC and private subnets
- **Database**: Enable encryption at rest
- **API**: Add rate limiting and authentication
- **Logging**: Sanitize sensitive data
- **Dependencies**: Regular security updates

## Cost Questions

### Q: What if I want to upgrade?
**A:** Estimated costs for production:
- **Kafka**: Confluent Cloud ~$100/month
- **Database**: AWS RDS ~$50/month
- **Compute**: AWS ECS ~$30/month
- **Monitoring**: Datadog ~$15/month
- **Total**: ~$200/month for production-grade

### Q: Can I monetize this?
**A:** Possible monetization:
- Sell API access to processed data
- Create premium dashboard with alerts
- Offer custom analytics
- Build trading signals service
- Consult on similar projects

## Learning Questions

### Q: What should I learn next?
**A:** Based on this project:
- **Advanced Kafka**: Kafka Streams, ksqlDB
- **Machine Learning**: Price prediction, anomaly detection
- **DevOps**: Kubernetes, Terraform, monitoring
- **Data Engineering**: Apache Spark, Airflow
- **Backend**: FastAPI, GraphQL
- **Frontend**: React, Vue.js for custom dashboard

### Q: What resources do you recommend?
**A:**
- **Kafka**: Confluent tutorials, "Kafka: The Definitive Guide"
- **Streaming**: "Streaming Systems" by Tyler Akidau
- **Python**: "Fluent Python" by Luciano Ramalho
- **System Design**: "Designing Data-Intensive Applications"
- **DevOps**: "The Phoenix Project"

## Troubleshooting

### Q: Producer won't connect to Kafka
**A:**
1. Verify credentials in `.env`
2. Check Upstash cluster is running
3. Test connection: `telnet your-cluster.upstash.io 9092`
4. Check firewall settings
5. Review producer logs

### Q: Consumer not processing messages
**A:**
1. Check Kafka topic has messages (Upstash console)
2. Verify database connection
3. Check consumer group status
4. Review consumer logs
5. Restart consumer

### Q: Dashboard shows no data
**A:**
1. Check database has data: `SELECT COUNT(*) FROM trades;`
2. Verify DATABASE_URL in Streamlit secrets
3. Check dashboard logs
4. Clear browser cache
5. Restart dashboard

### Q: GitHub Actions failing
**A:**
1. Check all secrets are set
2. Review workflow logs
3. Verify requirements.txt is correct
4. Check Python version (3.11+)
5. Test locally first

## Contributing

### Q: Can I contribute to this project?
**A:** Yes! Contributions welcome:
1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request
5. Follow code style guidelines

### Q: How do I report bugs?
**A:** Create a GitHub issue with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Logs/screenshots

## Support

### Q: Where can I get help?
**A:**
- **Documentation**: See README.md, ARCHITECTURE.md
- **Issues**: Create GitHub issue
- **Community**: Join discussions on GitHub
- **Email**: [Your email if you want]

### Q: Is there a community?
**A:** You can:
- Star the repository on GitHub
- Join discussions
- Share your improvements
- Help others in issues

---

**Still have questions?** Create an issue on GitHub or check the documentation files!
