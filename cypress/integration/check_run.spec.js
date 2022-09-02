context('Check Run List', () => {
	before(() => {
		cy.visit('/login')
		cy.login()
		cy.go_to_list('Check Run')
	})

	it("Add Check Run", () => {  // TEST WORKS
		cy.get('.primary-action').contains('Add Check Run').should('be.visible').click()
		cy.wait(1000)
		cy.get_field('company').focus().should('be.visible')  // May not be grabbing field from modal, but background table
		cy.get_field('bank_account').focus().should('be.visible')
		cy.get_field('pay_to_account').focus().should('be.visible')  // May not be grabbing field from modal, but background table
		cy.get('.btn-primary').contains('Start Check Run').should('be.visible').click()
	})

	it("Confirm Default Check Run Settings", () => {  // TEST WORKS
		cy.wait(1000)
		cy.get_open_dialog().contains('Yes').should('be.visible').click()
		cy.wait(1000)
		cy.get_field('include_purchase_invoices').should('be.checked')
		cy.get_field('include_journal_entries').should('be.checked')
		cy.get_field('include_expense_claims').should('be.checked')
		cy.get_field('pre_check_overdue_items').should('not.be.checked')
		cy.get_field('allow_cancellation').should('not.be.checked')
		cy.get_field('cascade_cancellation').should('not.be.checked')
		cy.get_field('number_of_invoices_per_voucher').should('have.value', 0)
		cy.get_field('ach_file_extension').should('have.value', 'ach')
		cy.get_field('ach_service_class_code', 'Select').find('option:selected').should('have.text', '200')
		cy.get_field('ach_standard_class_code', 'Select').find('option:selected').should('have.text', 'PPD')
		cy.get_field('ach_description').should('be.empty')
		cy.get('.btn-primary').contains('Save').should('be.visible').click().wait(500)
		cy.go('back')
	})

	it("Complete First Check Run", () => {  // TEST WORKS
		cy.wait(3000)
		// cy.visit('/app/check-run/ACC-CR-2022-00001')  // Throwing 403 Forbidden error when run in sequence
		cy.fill_field('end_date', '1/1', 'Date').blur()
		cy.fill_field('posting_date', '1/1', 'Date').blur()
		cy.wait(1000)  // Let date field change register
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

	it("Create Check Run Settings From List", () => {  // TEST WORKS
		cy.visit('/login')  // Re-login to avoid 403 Forbidden errors
		cy.login()
		cy.go_to_list('Check Run Settings')
		cy.wait(1000)
		cy.get('.primary-action').contains('Add Check Run Settings').should('be.visible').click()
		cy.wait(1000)
		cy.fill_field('bank_account', 'Primary Checking - Local Bank').blur().wait(500)
		cy.fill_field('pay_to_account', '2120 - Payroll Payable - CFC').blur().wait(500)
		cy.get('.btn-primary').contains('Save').should('be.visible').click()
	})

	it("Complete Payroll Check Run", () => {  // TEST WORKS
		cy.wait(3000)
		cy.go_to_list('Check Run')
		cy.get('.primary-action').contains('Add Check Run').should('be.visible').click()
		cy.wait(1000)
		cy.get('.modal [data-fieldname="pay_to_account"] input').clear().type('2120 - Payroll Payable - CFC').blur()
		cy.get('.btn-primary').contains('Start Check Run').should('be.visible').click()
		cy.fill_field('end_date', '1/1', 'Date').blur()
		cy.fill_field('posting_date', '1/1', 'Date').blur()
		cy.wait(1000)  // Let date field change register
		cy.get('#select-all').click()
		cy.get('.primary-action').contains('Save').should('be.visible').click()
		cy.get('.primary-action').contains('Submit').should('be.visible').click().wait(250)
		cy.get_open_dialog().contains('Yes').should('be.visible').click()
		cy.get('.indicator-pill').should('contain', 'Submitted').wait(250)
		cy.get('.indicator-pill').should('contain', 'Ready to Print').wait(7000)
	})
})