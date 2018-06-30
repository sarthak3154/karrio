import unittest
from gds_helpers import to_xml, jsonify, export
from openship.mappers.fedex import FedexClient, FedexProxy
from openship.domain.entities import Tracking
from openship.mappers.fedex.fedex_proxy import _create_envelope, _export_envolope 

proxy = FedexProxy(FedexClient(
  "https://wsbeta.fedex.com:443/web-services",
  "user_key",
  "password",
  "2349857",
  "1293587",
  "carrier_name"  
))


class TestFeDexMapper(unittest.TestCase):

    def test_error_parsing(self):
        parsed_response = proxy.mapper.parse_error_response(to_xml(AuthError))
      
        self.assertEqual(jsonify(parsed_response), jsonify(ParsedAuthError))

    def test_create_tracking_request(self):
        payload = Tracking.create(tracking_numbers=["794887075005"])
        tracking_req_xml_obj = proxy.mapper.create_tracking_request(payload)
        envelope_= _create_envelope(tracking_req_xml_obj)
        xmlStr = _export_envolope(
            envelope_, 
            envelope_prefix='soapenv:', 
            child_name='TrackRequest', 
            child_prefix='v14:',
            namespacedef_='xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v14="http://fedex.com/ws/track/v14"'
        )

        self.assertEqual(strip(xmlStr), strip(TrackingRequestXml))

    def test_parse_tracking_response(self):
      parsed_response = proxy.mapper.parse_tracking_response(to_xml(TrackingResponseXml))
      
      self.assertEqual(jsonify(parsed_response), jsonify(ParsedTrackingResponse))


def strip(text):
  return text.replace('\t','').replace('\n','').replace(' ','')

if __name__ == '__main__':
    unittest.main()





ParsedAuthError = [
    {
        "carrier": "carrier_name",
        "code": "1000",
        "message": "Authentication Failed"
    }
]

ParsedTrackingResponse = [
    [
        {
            "carrier": "carrier_name",
            "events": [
                {
                    "code": "OC",
                    "date": "2016-11-17 03:13:01-06:00",
                    "description": "Shipment information sent to FedEx",
                    "location": "CUSTOMER",
                    "signatory": None,
                    "time": None
                }
            ],
            "shipment_date": "2016-11-17 00:00:00",
            "tracking_number": "794887075005"
        }
    ],
    []
]


AuthError = '''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Header/>
    <SOAP-ENV:Body>
        <v14:TrackReply xmlns:v14="http://fedex.com/ws/track/v14">
            <v14:HighestSeverity xmlns:v14="http://fedex.com/ws/track/v14">ERROR</v14:HighestSeverity>
            <v14:Notifications xmlns:v14="http://fedex.com/ws/track/v14">
                <v14:Severity xmlns:v14="http://fedex.com/ws/track/v14">ERROR</v14:Severity>
                <v14:Source xmlns:v14="http://fedex.com/ws/track/v14">prof</v14:Source>
                <v14:Code xmlns:v14="http://fedex.com/ws/track/v14">1000</v14:Code>
                <v14:Message xmlns:v14="http://fedex.com/ws/track/v14">Authentication Failed</v14:Message>
            </v14:Notifications>
            <v14:TransactionDetail xmlns:v14="http://fedex.com/ws/track/v14">
                <v14:CustomerTransactionId xmlns:v14="http://fedex.com/ws/track/v14">Track By Number_v14</v14:CustomerTransactionId>
                <v14:Localization xmlns:v14="http://fedex.com/ws/track/v14">
                    <v14:LanguageCode xmlns:v14="http://fedex.com/ws/track/v14">EN</v14:LanguageCode>
                    <v14:LocaleCode xmlns:v14="http://fedex.com/ws/track/v14">US</v14:LocaleCode>
                </v14:Localization>
            </v14:TransactionDetail>
            <v14:Version xmlns:v14="http://fedex.com/ws/track/v14">
                <v14:ServiceId xmlns:v14="http://fedex.com/ws/track/v14">trck</v14:ServiceId>
                <v14:Major xmlns:v14="http://fedex.com/ws/track/v14">14</v14:Major>
                <v14:Intermediate xmlns:v14="http://fedex.com/ws/track/v14">0</v14:Intermediate>
                <v14:Minor xmlns:v14="http://fedex.com/ws/track/v14">0</v14:Minor>
            </v14:Version>
        </v14:TrackReply>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
'''

TrackingRequestXml = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v14="http://fedex.com/ws/track/v14">
   <soapenv:Body>
      <v14:TrackRequest>
         <v14:WebAuthenticationDetail>
            <v14:UserCredential>
               <v14:Key>user_key</v14:Key>
               <v14:Password>password</v14:Password>
            </v14:UserCredential>
         </v14:WebAuthenticationDetail>
         <v14:ClientDetail>
            <v14:AccountNumber>2349857</v14:AccountNumber>
            <v14:MeterNumber>1293587</v14:MeterNumber>
         </v14:ClientDetail>
         <v14:TransactionDetail>
            <v14:CustomerTransactionId>Track By Number_v14</v14:CustomerTransactionId>
            <v14:Localization>
               <v14:LanguageCode>en</v14:LanguageCode>
            </v14:Localization>
         </v14:TransactionDetail>
         <v14:Version>
            <v14:ServiceId>trck</v14:ServiceId>
            <v14:Major>14</v14:Major>
            <v14:Intermediate>0</v14:Intermediate>
            <v14:Minor>0</v14:Minor>
         </v14:Version>
         <v14:SelectionDetails>
            <v14:CarrierCode>FDXE</v14:CarrierCode>
            <v14:PackageIdentifier>
               <v14:Type>TRACKING_NUMBER_OR_DOORTAG</v14:Type>
               <v14:Value>794887075005</v14:Value>
            </v14:PackageIdentifier>
         </v14:SelectionDetails>
      </v14:TrackRequest>
   </soapenv:Body>
</soapenv:Envelope>
'''

TrackingResponseXml = '''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
   <SOAP-ENV:Header/>
   <SOAP-ENV:Body>
      <TrackReply xmlns="http://fedex.com/ws/track/v14">
         <HighestSeverity>SUCCESS</HighestSeverity>
         <Notifications>
            <Severity>SUCCESS</Severity>
            <Source>trck</Source>
            <Code>0</Code>
            <Message>Request was successfully processed.</Message>
            <LocalizedMessage>Request was successfully processed.</LocalizedMessage>
         </Notifications>
         <TransactionDetail>
            <CustomerTransactionId>Track By Number_v14</CustomerTransactionId>
            <Localization>
               <LanguageCode>EN</LanguageCode>
               <LocaleCode>US</LocaleCode>
            </Localization>
         </TransactionDetail>
         <Version>
            <ServiceId>trck</ServiceId>
            <Major>14</Major>
            <Intermediate>0</Intermediate>
            <Minor>0</Minor>
         </Version>
         <CompletedTrackDetails>
            <HighestSeverity>SUCCESS</HighestSeverity>
            <Notifications>
               <Severity>SUCCESS</Severity>
               <Source>trck</Source>
               <Code>0</Code>
               <Message>Request was successfully processed.</Message>
               <LocalizedMessage>Request was successfully processed.</LocalizedMessage>
            </Notifications>
            <DuplicateWaybill>false</DuplicateWaybill>
            <MoreData>false</MoreData>
            <TrackDetailsCount>0</TrackDetailsCount>
            <TrackDetails>
               <Notification>
                  <Severity>SUCCESS</Severity>
                  <Source>trck</Source>
                  <Code>0</Code>
                  <Message>Request was successfully processed.</Message>
                  <LocalizedMessage>Request was successfully processed.</LocalizedMessage>
               </Notification>
               <TrackingNumber>794887075005</TrackingNumber>
               <TrackingNumberUniqueIdentifier>2457710000~794887075005~FX</TrackingNumberUniqueIdentifier>
               <StatusDetail>
                  <CreationTime>2016-11-17T00:00:00</CreationTime>
                  <Code>OC</Code>
                  <Description>Shipment information sent to FedEx</Description>
                  <Location>
                     <Residential>false</Residential>
                  </Location>
                  <AncillaryDetails>
                     <Reason>IN001</Reason>
                     <ReasonDescription>Please check back later for shipment status or subscribe for e-mail notifications</ReasonDescription>
                  </AncillaryDetails>
               </StatusDetail>
               <ServiceCommitMessage>Shipping label has been created. The status will be updated when shipment begins to travel.</ServiceCommitMessage>
               <DestinationServiceArea>OC</DestinationServiceArea>
               <CarrierCode>FDXE</CarrierCode>
               <OperatingCompanyOrCarrierDescription>FedEx Express</OperatingCompanyOrCarrierDescription>
               <OtherIdentifiers>
                  <PackageIdentifier>
                     <Type>INVOICE</Type>
                     <Value>IO10570705</Value>
                  </PackageIdentifier>
               </OtherIdentifiers>
               <OtherIdentifiers>
                  <PackageIdentifier>
                     <Type>PURCHASE_ORDER</Type>
                     <Value>PO10570705</Value>
                  </PackageIdentifier>
               </OtherIdentifiers>
               <OtherIdentifiers>
                  <PackageIdentifier>
                     <Type>SHIPPER_REFERENCE</Type>
                     <Value>CUSTREF10570705</Value>
                  </PackageIdentifier>
               </OtherIdentifiers>
               <Service>
                  <Type>PRIORITY_OVERNIGHT</Type>
                  <Description>FedEx Priority Overnight</Description>
                  <ShortDescription>PO</ShortDescription>
               </Service>
               <PackageWeight>
                  <Units>LB</Units>
                  <Value>60.0</Value>
               </PackageWeight>
               <PackageDimensions>
                  <Length>12</Length>
                  <Width>12</Width>
                  <Height>12</Height>
                  <Units>IN</Units>
               </PackageDimensions>
               <ShipmentWeight>
                  <Units>LB</Units>
                  <Value>60.0</Value>
               </ShipmentWeight>
               <Packaging>Your Packaging</Packaging>
               <PackagingType>YOUR_PACKAGING</PackagingType>
               <PackageSequenceNumber>1</PackageSequenceNumber>
               <PackageCount>1</PackageCount>
               <SpecialHandlings>
                  <Type>DELIVER_WEEKDAY</Type>
                  <Description>Deliver Weekday</Description>
                  <PaymentType>OTHER</PaymentType>
               </SpecialHandlings>
               <Payments>
                  <Classification>TRANSPORTATION</Classification>
                  <Type>SHIPPER_ACCOUNT</Type>
                  <Description>Shipper</Description>
               </Payments>
               <ShipperAddress>
                  <City>COLORADO SPRINGS</City>
                  <StateOrProvinceCode>CO</StateOrProvinceCode>
                  <CountryCode>US</CountryCode>
                  <CountryName>United States</CountryName>
                  <Residential>false</Residential>
               </ShipperAddress>
               <DatesOrTimes>
                  <Type>ANTICIPATED_TENDER</Type>
                  <DateOrTimestamp>2016-11-17T00:00:00</DateOrTimestamp>
               </DatesOrTimes>
               <DestinationAddress>
                  <City>DENVER</City>
                  <StateOrProvinceCode>CO</StateOrProvinceCode>
                  <CountryCode>US</CountryCode>
                  <CountryName>United States</CountryName>
                  <Residential>false</Residential>
               </DestinationAddress>
               <DeliveryAttempts>0</DeliveryAttempts>
               <TotalUniqueAddressCountInConsolidation>0</TotalUniqueAddressCountInConsolidation>
               <NotificationEventsAvailable>ON_DELIVERY</NotificationEventsAvailable>
               <NotificationEventsAvailable>ON_EXCEPTION</NotificationEventsAvailable>
               <NotificationEventsAvailable>ON_ESTIMATED_DELIVERY</NotificationEventsAvailable>
               <NotificationEventsAvailable>ON_TENDER</NotificationEventsAvailable>
               <DeliveryOptionEligibilityDetails>
                  <Option>INDIRECT_SIGNATURE_RELEASE</Option>
                  <Eligibility>INELIGIBLE</Eligibility>
               </DeliveryOptionEligibilityDetails>
               <DeliveryOptionEligibilityDetails>
                  <Option>REDIRECT_TO_HOLD_AT_LOCATION</Option>
                  <Eligibility>INELIGIBLE</Eligibility>
               </DeliveryOptionEligibilityDetails>
               <DeliveryOptionEligibilityDetails>
                  <Option>REROUTE</Option>
                  <Eligibility>INELIGIBLE</Eligibility>
               </DeliveryOptionEligibilityDetails>
               <DeliveryOptionEligibilityDetails>
                  <Option>RESCHEDULE</Option>
                  <Eligibility>INELIGIBLE</Eligibility>
               </DeliveryOptionEligibilityDetails>
               <Events>
                  <Timestamp>2016-11-17T03:13:01-06:00</Timestamp>
                  <EventType>OC</EventType>
                  <EventDescription>Shipment information sent to FedEx</EventDescription>
                  <Address>
                     <Residential>false</Residential>
                  </Address>
                  <ArrivalLocation>CUSTOMER</ArrivalLocation>
               </Events>
            </TrackDetails>
         </CompletedTrackDetails>
      </TrackReply>
   </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
'''