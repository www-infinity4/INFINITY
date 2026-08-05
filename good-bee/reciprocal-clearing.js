const els = {
  menuButton: document.querySelector('#menuButton'),
  mainNav: document.querySelector('#mainNav'),
  form: document.querySelector('#clearingForm'),
  claimValue: document.querySelector('#claimValue'),
  exchangeRate: document.querySelector('#exchangeRate'),
  reserveRate: document.querySelector('#reserveRate'),
  communityRate: document.querySelector('#communityRate'),
  operationsRate: document.querySelector('#operationsRate'),
  receiptStatus: document.querySelector('#receiptStatus'),
  receiptRows: document.querySelector('#receiptRows'),
  receiptWarning: document.querySelector('#receiptWarning'),
  year: document.querySelector('#year')
}

function numberValue(input) {
  const value = Number(input.value)
  return Number.isFinite(value) && value >= 0 ? value : 0
}

function fmt(value) {
  return new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 }).format(value)
}

function renderReceipt(event) {
  event?.preventDefault()

  const claim = numberValue(els.claimValue)
  const rate = numberValue(els.exchangeRate)
  const reserveRate = numberValue(els.reserveRate)
  const communityRate = numberValue(els.communityRate)
  const operationsRate = numberValue(els.operationsRate)
  const totalRate = reserveRate + communityRate + operationsRate

  if (totalRate > 100) {
    els.receiptStatus.textContent = 'Demonstration blocked'
    els.receiptRows.innerHTML = ''
    els.receiptWarning.textContent = `Combined deductions are ${fmt(totalRate)}%, which exceeds 100%.`
    return
  }

  const gross = claim * rate
  const reserve = gross * reserveRate / 100
  const community = gross * communityRate / 100
  const operations = gross * operationsRate / 100
  const wallet = Math.max(0, gross - reserve - community - operations)

  els.receiptStatus.textContent = claim > 0 ? 'Source claim retired before issuance' : 'No claim entered'
  els.receiptRows.innerHTML = `
    <div class="receipt-row"><span>Verified source claim</span><strong>${fmt(claim)} store units</strong></div>
    <div class="receipt-row"><span>Published demonstration rate</span><strong>${fmt(rate)} Infinity units per claim unit</strong></div>
    <div class="receipt-row retired"><span>Store claim status</span><strong>${claim > 0 ? 'LOCKED + RETIRED' : 'NOT ISSUED'}</strong></div>
    <div class="receipt-row"><span>Gross replacement amount</span><strong>${fmt(gross)}</strong></div>
    <div class="receipt-row"><span>Settlement reserve</span><strong>${fmt(reserve)}</strong></div>
    <div class="receipt-row"><span>Community pool</span><strong>${fmt(community)}</strong></div>
    <div class="receipt-row"><span>Operations/tax allocation</span><strong>${fmt(operations)}</strong></div>
    <div class="receipt-row issued"><span>Infinity units issued to wallet</span><strong>${fmt(wallet)}</strong></div>
  `
  els.receiptWarning.textContent = 'Illustration only. A real exchange rate and every allocation require funding, contracts, legal review, disclosures, and an auditable policy.'
}

function bindNavigation() {
  els.menuButton?.addEventListener('click', () => {
    const open = els.mainNav.classList.toggle('open')
    els.menuButton.setAttribute('aria-expanded', String(open))
  })

  els.mainNav?.addEventListener('click', event => {
    if (event.target.matches('a')) {
      els.mainNav.classList.remove('open')
      els.menuButton?.setAttribute('aria-expanded', 'false')
    }
  })
}

function init() {
  bindNavigation()
  els.form?.addEventListener('submit', renderReceipt)
  ;[els.claimValue, els.exchangeRate, els.reserveRate, els.communityRate, els.operationsRate]
    .forEach(input => input?.addEventListener('input', renderReceipt))
  els.year.textContent = new Date().getFullYear()
  renderReceipt()
}

init()
