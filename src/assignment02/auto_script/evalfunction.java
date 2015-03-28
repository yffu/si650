package com.example.tests;

import java.util.regex.Pattern;
import java.util.concurrent.TimeUnit;
import org.junit.*;
import static org.junit.Assert.*;
import static org.hamcrest.CoreMatchers.*;
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.Select;

public class Evalfunction {
  private WebDriver driver;
  private String baseUrl;
  private boolean acceptNextAlert = true;
  private StringBuffer verificationErrors = new StringBuffer();

  @Before
  public void setUp() throws Exception {
    driver = new FirefoxDriver();
    baseUrl = "http://infolab.ece.udel.edu:8008/";
    driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
  }

  @Test
  public void testEvalfunction() throws Exception {
    driver.findElement(By.linkText("Manage Function")).click();
    driver.findElement(By.xpath("(//button[@id='trial_00'])[3]")).click();
    driver.findElement(By.id("1,76394")).click();
    assertEquals("The evaluation may take several minutes! Thanks for your patient!", closeAlertAndGetItsText());
    driver.findElement(By.id("4,76394")).click();
    assertEquals("The evaluation may take several minutes! Thanks for your patient!", closeAlertAndGetItsText());
    driver.findElement(By.id("5,76394")).click();
    assertEquals("The evaluation may take several minutes! Thanks for your patient!", closeAlertAndGetItsText());
    driver.findElement(By.id("6,76394")).click();
    assertEquals("The evaluation may take several minutes! Thanks for your patient!", closeAlertAndGetItsText());
    driver.get(baseUrl + "/VIRLab_UMich/home.php");
  }

  @After
  public void tearDown() throws Exception {
    driver.quit();
    String verificationErrorString = verificationErrors.toString();
    if (!"".equals(verificationErrorString)) {
      fail(verificationErrorString);
    }
  }

  private boolean isElementPresent(By by) {
    try {
      driver.findElement(by);
      return true;
    } catch (NoSuchElementException e) {
      return false;
    }
  }

  private boolean isAlertPresent() {
    try {
      driver.switchTo().alert();
      return true;
    } catch (NoAlertPresentException e) {
      return false;
    }
  }

  private String closeAlertAndGetItsText() {
    try {
      Alert alert = driver.switchTo().alert();
      String alertText = alert.getText();
      if (acceptNextAlert) {
        alert.accept();
      } else {
        alert.dismiss();
      }
      return alertText;
    } finally {
      acceptNextAlert = true;
    }
  }
}
