"""High-level Device base class implementation."""


class Device:
    """A Device represents a physical object being managed by an Adapter."""

    def __init__(self, adapter, _id):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        _id -- the device's individual ID
        """
        self.adapter = adapter
        self.id = _id
        self.type = 'thing'
        self.name = ''
        self.description = ''
        self.properties = {}
        self.actions = {}

    def as_dict(self):
        """
        Get the device state as a dictionary.

        Returns the state as a dictionary.
        """
        properties = {k: v.as_dict() for k, v in self.properties.items()}
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'properties': properties,
            'actions': self.actions,
        }

    def as_thing(self):
        """
        Return the device state as a Thing Description.

        Returns the state as a dictionary.
        """
        thing = {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'properties': self.get_property_descriptions(),
        }

        if self.description:
            thing['description'] = self.description

        return thing

    def get_id(self):
        """
        Get the ID of the device.

        Returns the ID as a string.
        """
        return self.id

    def get_name(self):
        """
        Get the name of the device.

        Returns the name as a string.
        """
        return self.name

    def get_type(self):
        """
        Get the type of the device.

        Returns the type as a string.
        """
        return self.type

    def get_property_descriptions(self):
        """
        Get the device's properties as a dictionary.

        Returns the properties as a dictionary, i.e. name -> description.
        """
        return {k: v.as_property_description()
                for k, v in self.properties.items()}

    def find_property(self, property_name):
        """
        Find a property by name.

        property_name -- the property to find

        Returns a Property object, if found, else None.
        """
        return self.properties.get(property_name, None)

    def get_property(self, property_name):
        """
        Get a property's value.

        property_name -- the property to get the value of

        Returns the properties value, if found, else None.
        """
        prop = self.find_property(property_name)
        if prop:
            return prop.get_value()

        return None

    def has_property(self, property_name):
        """
        Determine whether or not this device has a given property.

        property_name -- the property to look for

        Returns a boolean, indicating whether or not the device has the
        property.
        """
        return property_name in self.properties

    def notify_property_changed(self, prop):
        """
        Notify the AddonManager in the Gateway that a device property changed.

        prop -- the property that changed
        """
        self.adapter.manager_proxy.send_property_changed_notification(prop)

    def set_property(self, property_name, value):
        """
        Set a property value.

        property_name -- name of the property to set
        value -- value to set
        """
        prop = self.find_property(property_name)
        if not prop:
            return

        prop.set_value(value)
