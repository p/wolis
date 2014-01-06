# depends:
# python.install
#
# after:
# python.login

utils = require './utils'

d = ->
  console.log arguments...

base = global.wolis.config.test_url

casper.start()

c2 = require('casper').create()

casper.then ->
  utils.login 'morpheus', 'morpheus',

casper.then ->
  @open base

utils.thensaveresponse ->
  @test.assertHttpStatus 200
  
  @test.assertTextExists 'Administration Control Panel'
  @click utils.xpath(utils.a_text_xpath('Administration Control Panel'))

utils.thensaveresponse ->
  @test.assertHttpStatus 200
  
  @test.assertTextExists 'To administer the board you must re-authenticate yourself.'
  password_name = @evaluate ->
    document.querySelector('input[type=password]').getAttribute('name')
  
  @evaluate utils.fixsubmit, 'form#login'
  fields = {username: 'morpheus'}
  fields[password_name] = 'morpheus'
  @fill 'form#login', fields, true

c2.start()
utils.thensaveresponse ->
  d 'aa'
  c2.then ->
    d 'kk'
    @open base
  c2.then ->
    d 'zz'
    @test.assertTextExists 'Welcome'

utils.thensaveresponse ->
  @test.assertHttpStatus 200
  
  @test.assertTextExists 'Proceed to the ACP'
  @click utils.xpath(utils.a_text_xpath('Proceed to the ACP'))

utils.thensaveresponse ->
  @test.assertHttpStatus 200
  
  @test.assertTextExists 'Thank you for choosing phpBB as your board solution.'

casper.run ->
  c2.run ->
    @test.done()
    casper.test.done()
