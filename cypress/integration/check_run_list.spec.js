context('Check Run List', () => {
	before(() => {
		cy.visit('/login')
		cy.login()
		cy.go_to_list('Check Run')
	})

	it("Create a new Check Run", () => {
		cy.get('.primary-action').contains('Add Check Run').should('be.visible').click()
		cy.wait(500)
		cy.get_field('company').focus().should('be.visible')
		cy.get_field('bank_account').focus().should('be.visible')
		cy.get_field('pay_to_account').focus().should('be.visible')
		cy.fill_field("bank_account", "Primary Checking - Local Bank").blur()
		cy.fill_field("pay_to_account", "Local Bank - CFC").blur()
		cy.get('.btn-primary').contains('Save').should('be.visible').click()
	})
})