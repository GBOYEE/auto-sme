# Pilot Plan — AutoSME

**Goal:** Onboard 5 small businesses in Nigeria/Kenya/Ethiopia for a 4-week pilot, collect feedback, and iterate.

## Recruitment

- Use personal network, local business associations, or social media groups.
- Target businesses with simple inventory needs: retail shops, food vendors, small wholesalers.
- Aim for diversity: 2 in Lagos, 1 in Nairobi, 1 in Addis Ababa, 1 remote.

## Onboarding

For each SME:
1. Create tenant in the system (API call `POST /api/v1/inventory` to add their products).
2. Generate a unique API key for their admin (or provide dashboard later).
3. Register WhatsApp business number for order webhook (or use personal WhatsApp for pilot).
4. Send quick start guide (PDF or video) explaining:
   - How to add products (via API or dashboard if available)
   - How customers place orders via WhatsApp
   - How to view reports
5. Offer WhatsApp support channel for questions.

## Data Collection

- **Metrics to log automatically:**
  - Orders created, total revenue
  - Stock adjustments
  - API usage (requests per day)
- **User feedback:** After 2 weeks, send short survey (Google Forms):
  - How many hours saved per week?
  - Any bugs or confusing steps?
  - Would you pay $X/month?

## Support

- Monitor logs daily; fix critical issues within 24h.
- Keep a shared Telegram/WhatsApp group for pilot participants to chat.

## Success Criteria

- At least 4/5 SMEs actively using the system (placing orders weekly).
- Average satisfaction score >4/5.
- No critical bugs (data loss, incorrect stock) for >3 consecutive days.
- Capture testimonials and case study material (photos, quotes).

## Iteration

- Weekly team sync to review feedback and prioritize fixes.
- Push updates to pilot VPS after testing.

## After Pilot

- Compile impact metrics for grant reports.
- Transition to paid beta if applicable.
- Document lessons learned and adjust roadmap.
