from lxml import etree
import dicttoxml2
import json
import lxml
import utils.File as FileUtils
import xmltodict


class XmlHelper:
    def __init__(self):
        self.xml_object = None
        self.xml_successfully_loaded = False
        self.file_encoding = None

    def attribute_available(self, attribute_name: str, element_object: dict = None, element_xpath: str = None) -> bool:
        attribute_found = False
        if element_object is not None and element_xpath is None:
            try:
                attr_value = element_object.get(attribute_name)
                if attr_value is not None:
                    attribute_found = True
            except:
                pass
        elif element_object is None and element_xpath is not None:
            if self.element_available(element_xpath=element_xpath):
                attr_value = self.xml_object.xpath(element_xpath)[0].get(attribute_name)
                if attr_value is not None:
                    attribute_found = True

        return attribute_found

    def create_new(self, root_element: str) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}

        try:
            self.xml_object = lxml.etree.ElementTree(lxml.etree.Element(root_element))
            return_value['status'] = 'SUCCESS'
        except:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unable to create empty XML object'

        return return_value

    def element_add(self, element_name: str, parent_element_object: dict = None, parent_element_name: str = None, element_text: str = None, element_attributes=None) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}

        try:
            res_find_parent_element = None
            parent_element_found = False

            if element_attributes is None:
                element_attributes = []

            # Find parent element
            if parent_element_object is not None and parent_element_name is None:
                parent_element_found = True
                res_find_parent_element = parent_element_object
            elif parent_element_object is None and parent_element_name is not None:
                res_find_parent_element = self.get_element(element_name=parent_element_name)
                if res_find_parent_element['status'] == 'SUCCESS':
                    parent_element_found = True
                    res_find_parent_element = res_find_parent_element['response_body']
            else:
                parent_element_found = False

            # Create new element
            if parent_element_found:
                element = lxml.etree.SubElement(res_find_parent_element, element_name)

                # Add elementText
                if element_text is not None:
                    element.text = element_text

                # Add elementAttributes
                for attribute in element_attributes:
                    element.set(attribute['key'], attribute['value'])

                return_value['status'] = 'SUCCESS'
            else:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Unable to add element as requested parent element was not found'
        except:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unable to add element'

        return return_value

    def element_available(self, element_name: str = None, element_xpath: str = None) -> bool:
        element_found = False

        try:
            if element_name is not None and element_xpath is None:
                element_found = False
                try:
                    root = self.xml_object.getroot()
                except:
                    root = self.xml_object
                for _ in root.iter(element_name):
                    element_found = True
            elif element_name is None and element_xpath is not None:
                target = self.xml_object.xpath(element_xpath)
                if target:
                    element_found = True
            else:
                element_found = False
        except:
            element_found = False

        return element_found

    def element_delete(self, element_xpath: str = None) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}

        try:
            if self.element_available(element_xpath=element_xpath):
                el = self.get_element(element_xpath=element_xpath)['response_body']
                el.getparent().remove(el)
                if not self.xml_object.element_available(element_xpath=element_xpath):
                    return_value['status'] = 'SUCCESS'
                else:
                    return_value['status'] = 'FAILED'
                    return_value['error_message'] = 'Unable to confirm if element was'
            else:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Element does not exist'
        except:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unexpected error when deleting element'

        return return_value

    def get_as_dict(self) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}

        try:
            if self.file_encoding is None:
                xml_string = lxml.etree.tostring(self.xml_object).decode()
            else:
                xml_string = lxml.etree.tostring(self.xml_object).decode(str(self.file_encoding))

            s_dict = xmltodict.parse(xml_string)
            json_string = json.dumps(s_dict)
            return_value['status'] = 'SUCCESS'
            return_value['response_body'] = json.loads(json_string)
        except:
            return_value['status'] = 'SUCCESS'
            return_value['error_message'] = 'Unable to retrieve dict'
        return return_value

    def get_as_xml(self) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}

        try:
            return_value['status'] = 'SUCCESS'
            return_value['response_body'] = self.xml_object
        except:
            return_value['status'] = 'SUCCESS'
            return_value['error_message'] = 'Unable to retrieve xml'

        return return_value

    def get_as_xml_string(self) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}

        try:
            return_value['status'] = 'SUCCESS'
            return_value['response_body'] = etree.tostring(self.xml_object, pretty_print=True, encoding=str)
        except:
            return_value['status'] = 'SUCCESS'
            return_value['error_message'] = 'Unable to retrieve xml'

        return return_value

    def get_attribute_value(self, element_object: dict = None, element_xpath: str = None, attribute_name: str = None) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': []}

        if element_object is not None and element_xpath is None:
            try:
                return_value['status'] = 'SUCCESS'
                if attribute_name is None:
                    attributes = element_object.items()
                    attr_list = []
                    for attr in attributes:
                        attr_list.append({'key': attr[0], 'value': attr[1]})
                    return_value['response_body'] = attr_list
                else:
                    attr_value = element_object.get(attribute_name)
                    if attr_value is not None:
                        return_value['response_body'].append({'key': attribute_name, 'value': attr_value})
            except:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Element does not exist'
        elif element_object is None and element_xpath is not None:
            if self.element_available(element_xpath=element_xpath):
                return_value['status'] = 'SUCCESS'
                if attribute_name is None:
                    attributes = self.xml_object.xpath(element_xpath)[0].items()
                    attr_list = []
                    for attr in attributes:
                        attr_list.append({'key': attr[0], 'value': attr[1]})
                    return_value['response_body'] = attr_list
                else:
                    attr_value = self.xml_object.xpath(element_xpath)[0].get(attribute_name)
                    if attr_value is not None:
                        return_value['response_body'].append({'key': attribute_name, 'value': attr_value})
            else:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Element does not exist'
        else:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'You must supply an element_name OR and XPath'

        return return_value

    def get_element(self, element_name: str = None, element_xpath: str = None) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}

        try:
            target = None

            if element_name is not None and element_xpath is None:
                element_found = False
                try:
                    root = self.xml_object.getroot()
                except:
                    root = self.xml_object
                for element in root.iter(element_name):
                    element_found = True
                    target = element

                if element_found:
                    return_value['status'] = 'SUCCESS'
                    return_value['response_body'] = target
                else:
                    return_value['status'] = 'FAILED'
                    return_value['error_message'] = 'Requested element not found'
            elif element_name is None and element_xpath is not None:
                target = self.xml_object.xpath(element_xpath)
                if target:
                    return_value['status'] = 'SUCCESS'
                    return_value['response_body'] = target[0]
                else:
                    return_value['status'] = 'FAILED'
                    return_value['error_message'] = 'Requested element not found'
            else:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'You must supply an element_name OR and XPath'
        except:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unable to search element'

        return return_value

    def get_element_value(self, element_object: dict = None, element_xpath: str = None) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}

        if element_object is not None and element_xpath is None:
            try:
                return_value['status'] = 'SUCCESS'
                # noinspection PyUnresolvedReferences
                return_value['response_body'] = element_object.text
            except:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Element does not exist'
        elif element_object is None and element_xpath is not None:
            if self.element_available(element_xpath=element_xpath):
                return_value['status'] = 'SUCCESS'
                return_value['response_body'] = self.xml_object.xpath(element_xpath)[0].text
            else:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Element does not exist'
        else:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'You must supply an element_name OR and XPath'

        return return_value

    def load_dict(self, xml_dict: dict) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}

        try:
            tmp_object = dicttoxml2.dicttoxml(xml_dict, attr_type=False)
            self.xml_object = etree.fromstring(tmp_object)
            self.xml_successfully_loaded = True
            return_value['status'] = 'SUCCESS'
        except:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unable to parse dict as XML object'

        return return_value

    def load_file(self, full_file_path: str, path_is_url: bool = False) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}

        if FileUtils.file_exists(full_file_path=full_file_path, path_is_url=path_is_url):
            try:
                self.xml_object = lxml.etree.parse(full_file_path)
                self.xml_successfully_loaded = True
                return_value['status'] = 'SUCCESS'
            except:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Unable to parse file as XML object'
        else:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'File does not exist'

        return return_value

    def print_to_console(self):
        print(etree.tostring(self.xml_object, pretty_print=True, encoding=str))

    def save(self, full_file_path: str, overwrite: bool = True) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}

        try:
            if FileUtils.file_exists(full_file_path=full_file_path, path_is_url=False) and not overwrite:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Unable to save XML file as file already exists'
            else:
                if self.file_encoding is None:
                    self.xml_object.write(full_file_path)
                else:
                    self.xml_object.write(full_file_path, xml_declaration=True, encoding=str(self.file_encoding))
                return_value['status'] = 'SUCCESS'
        except:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unable to save XML file'

        return return_value

    def set_element_value(self, element_object: dict = None, element_xpath: str = None, element_value: str = None) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}

        if element_object is not None and element_xpath is None:
            try:
                return_value['status'] = 'SUCCESS'
                element_object.text = element_value
            except:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Element does not exist'
        elif element_object is None and element_xpath is not None:
            if self.element_available(element_xpath=element_xpath):
                return_value['status'] = 'SUCCESS'
                self.xml_object.xpath(element_xpath)[0].text = element_value
            else:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Element does not exist'
        else:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'You must supply an element_name OR and XPath'

        return return_value

    def set_encoding(self, encoding: str = 'utf-8'):
        self.file_encoding = encoding

    def successfully_loaded(self):
        return self.xml_successfully_loaded


class XsdValidator:
    def __init__(self, xsd_full_file_path: str):
        xmlschema_doc = etree.parse(xsd_full_file_path)
        self.xmlschema = etree.XMLSchema(xmlschema_doc)

    def validate(self, xml_full_file_path: str) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': {}}
        return_value['response_body']['validation_status'] = ''
        return_value['response_body']['xml_file_name'] = ''
        return_value['response_body']['errors'] = []

        return_value['responseBody']['xml_file_name'] = xml_full_file_path

        try:
            xml_document = etree.parse(xml_full_file_path)
            validation_result = self.xmlschema.validate(xml_document)
            validation_err_log = self.xmlschema.error_log

            if validation_result:
                return_value['response_body']['validation_status'] = 'SUCCESS'
            else:
                return_value['response_body']['validation_status'] = 'FAILED'

            for error in validation_err_log:
                tmp_json_object_error = {'element_path': str(error.path), 'line': str(error.line), 'message': str(error.message)}
                return_value['response_body']['errors'].append(tmp_json_object_error)

            return_value['status'] = 'SUCCESS'
        except:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unable to parse XML file'

        return return_value


class DtdValidator:
    def __init__(self, dtd_full_file_path: str):
        self.dtdschema = etree.DTD(file=dtd_full_file_path)

    def validate(self, xml_full_file_path: str) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': {}}
        return_value['response_body']['validationStatus'] = ''
        return_value['response_body']['xml_file_name'] = ''
        return_value['response_body']['errors'] = []

        return_value['responseBody']['xml_file_name'] = xml_full_file_path

        try:
            xml_document = etree.parse(xml_full_file_path)
            validation_result = self.dtdschema.validate(xml_document)
            validation_err_log = self.dtdschema.error_log

            if validation_result:
                return_value['response_body']['validation_status'] = 'SUCCESS'
            else:
                return_value['response_body']['validation_status'] = 'FAILED'

            for error in validation_err_log:
                tmp_json_object_error = {'element_path': str(error.path), 'line': str(error.line), 'message': str(error.message)}
                return_value['response_body']['errors'].append(tmp_json_object_error)

            return_value['status'] = 'SUCCESS'
        except:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unable to parse XML file'

        return return_value
