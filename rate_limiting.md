Rate limiting is a mechanism where for a particular token twitter doesn't allow 100 request per hour.
This is throttling mechanism for the API usage.

Exceeding this rate_limit the calls after this will return response stating "rate limit exceeded" and until the
time span of 1 hour is been crossed all calls will get the same message. After 1 hour this value is reset to initial limit

