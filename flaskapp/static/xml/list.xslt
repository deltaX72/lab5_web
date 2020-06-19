<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version = "1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html>
    <head>
        <title>Drinks</title>
    </head>
    <body>
      <ul>
          <xsl:for-each select="drinks/drink">
          <li> 
              <xsl:value-of select="@id"/> &#160; <xsl:value-of select="name"/> &#160; <xsl:value-of select="volume"/> &#160; <xsl:value-of select="price"/>
          </li>
      </xsl:for-each>
      </ul>
    </body>
</html>
</xsl:template></xsl:stylesheet>
