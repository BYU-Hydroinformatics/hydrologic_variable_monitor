from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting
from tethys_sdk.permissions import Permission, PermissionGroup


class HydroVarMonitor(TethysAppBase):
    """
    Tethys app class for Hydrologic Trends Monitor.
    """

    name = 'Climate Trends'
    description = 'View maps and plots of hydrologic cycle variables recorded by satellites and global models'
    package = 'hydro_var_monitor'
    index = 'home'
    icon = f'{package}/images/logo.gif'
    root_url = 'hydro-var-monitor'
    color = '#6DA8D9'
    tags = ['remote sensing', 'earth engine', 'hydrological cycle', 'essential water variables', 'geoglows toolbox']
    enable_feedback = False
    feedback_emails = []
    controller_modules = ['controllers']

    # def url_maps(self):
    #     """
    #     Add controllers
    #     """
    #     UrlMap = url_map_maker(self.root_url)

    #     url_maps = (
    #         UrlMap(
    #             name='home',
    #             url=f'{self.root_url}',
    #             controller=f'{self.package}.controllers.home'
    #         ),

    #         UrlMap(
    #             name='get-map-id',
    #             url=f'{self.root_url}/get-map-id/',
    #             controller=f'{self.package}.controllers.get_map_id'
    #         ),
    #         UrlMap(
    #             name='get-plot',
    #             url=f'{self.root_url}/get-plot/',
    #             controller=f'{self.package}.controllers.get_plot'
    #         ),
    #         UrlMap(
    #             name='compare',
    #             url=f'{self.root_url}/compare/',
    #             controller=f'{self.package}.controllers.compare'
    #         ),
    #         UrlMap(
    #             name='compare_precip',
    #             url=f'{self.root_url}/compare-precip/',
    #             controller=f'{self.package}.controllers.compare_precip'
    #         ),
    #         UrlMap(
    #             name='get_predefined',
    #             url=f'{self.root_url}/get-predefined/',
    #             controller=f'{self.package}.controllers.get_predefined'
    #         ),
    #     )

    #     return url_maps

    def custom_settings(self):
        return (
            CustomSetting(
                name='ee_auth_token_path',
                type=CustomSetting.TYPE_STRING,
                description='Path to an earth engine service account auth token',
                required=False
            ),
        )

    from tethys_sdk.permissions import Permission, PermissionGroup

    class MyFirstApp(TethysAppBase):

        def permissions(self):
            """
            Example permissions method.
            """
            # Viewer Permissions
            admin_page = Permission(
                name='admin_page',
                description='Access Admin'
            )

            admin = PermissionGroup(
                name='admin',
                permissions=admin_page
            )

            permissions = admin

            return permissions
