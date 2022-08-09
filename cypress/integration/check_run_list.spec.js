context('Check Run List', () => {
	before(() => {
		cy.visit('/login')
		cy.login()
		cy.go_to_list('Check Run')
	})

	it("Add Check Run", () => {
		cy.get('.primary-action').contains('Add Check Run').should('be.visible').click()
		cy.wait(1000)
		cy.get_field('company').focus().should('be.visible')
		cy.get_field('bank_account').focus().should('be.visible')
		cy.get_field('pay_to_account').focus().should('be.visible')
		cy.get('.btn-primary').contains('Start Check Run').click()
	})
})