context('Check Run List', () => {
	before(() => {
		cy.visit('/login')
		cy.login()
		cy.go_to_list('Check Run')
		cy.get('.primary-action').contains('Add Check Run').should('be.visible').click()
	})
})