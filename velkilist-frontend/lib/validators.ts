export function isValidEmail(email: string): boolean {
  // Basic but robust email pattern compatible with most emails
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/
  return re.test(String(email).trim())
}
