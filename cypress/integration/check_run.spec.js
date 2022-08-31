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
		cy.get('.btn-primary').contains('Start Check Run').should('be.visible').click()
	})

	// Incorporate new 'Confirm settings' prompt
	it("Confirm Settings", () => {
		cy.get_open_dialog().contains('Yes').should('be.visible').click()
	})

	it("Complete First Check Run", () => {
		cy.visit('/app/check-run/ACC-CR-2022-00001')
		cy.fill_field("end_date", "1/1").blur()
		cy.fill_field("posting_date", "1/1").blur()
		cy.get('[data-checkbox-index="0"]').click().wait(250)
		cy.get('[data-fieldname="amount_check_run"]').get('.like-disabled-input').should('contain', '$ 1,800.00')
		cy.get('body').type(' ').wait(250)
		cy.get('[data-fieldname="amount_check_run"]').get('.like-disabled-input').should('contain', '$ 0.00').wait(250)
		cy.get('#select-all').click()
		cy.get('.primary-action').contains('Save').should('be.visible').click()
		cy.get('.primary-action').contains('Submit').should('be.visible').click().wait(250)
		cy.get_open_dialog().contains('Yes').should('be.visible').click()
		cy.get('.indicator-pill').should('contain', 'Submitted').wait(250)
		cy.get('.indicator-pill').should('contain', 'Ready to Print').wait(15000)
	})

	it("Complete Second Check Run", () => {
		cy.get('body').type('{ctrl+b}').wait(500)
		cy.fill_field("end_date", "1/1").blur()
		cy.fill_field("posting_date", "1/1").blur()
		cy.get_field("pay_to_account").type("{ctrl+home}{del}").blur().wait(100)
		cy.fill_field("pay_to_account", "2120 - Payroll Payable - CFC").blur().wait(500)
		cy.get('#select-all').click()
		cy.get('.primary-action').contains('Save').should('be.visible').click()
		cy.get('.primary-action').contains('Submit').should('be.visible').click().wait(250)
		cy.get_open_dialog().contains('Yes').should('be.visible').click()
		cy.get('.indicator-pill').should('contain', 'Submitted').wait(250)
		cy.get('.indicator-pill').should('contain', 'Ready to Print').wait(7000)
	})
})